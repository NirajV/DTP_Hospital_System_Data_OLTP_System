"""
Clinical Measurements API (v1)
==============================
Implements Appendix C.7.1 - C.7.4 of Requirement.md:

    POST   /api/v1/encounters/<encounter_id>/measurements
    POST   /api/v1/encounters/<encounter_id>/measurements:bulk
    GET    /api/v1/patients/<patient_id>/measurements
    PATCH  /api/v1/measurements/<measurement_id>

Scaffolding only. Audit-log writes and edit-window enforcement (CM-07)
are stubbed where the production logic belongs.
"""

import json
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

from flask import Blueprint, request, jsonify, g

from database_connection import DatabaseConnection
from api.auth import require_role


measurements_bp = Blueprint("measurements", __name__, url_prefix="/api/v1")

EDIT_WINDOW_HOURS = 24


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def _lookup_type(db, type_code: str):
    rows = db.execute_select(
        "SELECT type_id, default_unit_id, normal_range_low, normal_range_high "
        "FROM measurement_types WHERE type_code=%s AND is_active=1",
        (type_code,),
    )
    return rows[0] if rows else None


def _lookup_unit(db, unit_code: str):
    rows = db.execute_select(
        "SELECT unit_id FROM measurement_units WHERE unit_code=%s AND is_active=1",
        (unit_code,),
    )
    return rows[0] if rows else None


def _is_abnormal(value, low, high) -> bool:
    if value is None or (low is None and high is None):
        return False
    if low is not None and value < low:
        return True
    if high is not None and value > high:
        return True
    return False


def _write_audit(db, action: str, record_id: int, old: dict | None, new: dict | None):
    db.execute_query(
        "INSERT INTO audit_logs (table_name, record_id, action, user_id, user_type, "
        "old_values, new_values, ip_address, user_agent) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            "clinical_measurements",
            record_id,
            action,
            g.user_id,
            g.role,
            json.dumps(old, default=str) if old else None,
            json.dumps(new, default=str) if new else None,
            request.remote_addr,
            request.headers.get("User-Agent", "")[:500],
        ),
    )


def _persist_measurement(db, encounter_id: int, body: dict) -> tuple:
    """Returns (status_code, response_dict)."""
    type_code = body.get("type_code")
    unit_code = body.get("unit_code")
    value_numeric = body.get("value_numeric")
    value_text = body.get("value_text")
    notes = body.get("notes")

    if not type_code:
        return 400, {"error": "INVALID_TYPE", "detail": "type_code required"}
    if not unit_code:
        return 400, {"error": "INVALID_UNIT", "detail": "unit_code required"}
    if value_numeric is None and value_text is None:
        return 400, {"error": "MEASUREMENT_VALUE_REQUIRED"}

    if value_numeric is not None:
        try:
            value_numeric = Decimal(str(value_numeric))
        except InvalidOperation:
            return 400, {"error": "MEASUREMENT_VALUE_REQUIRED", "detail": "value_numeric not numeric"}

    enc = db.execute_select(
        "SELECT patient_id, status FROM encounters WHERE encounter_id=%s",
        (encounter_id,),
    )
    if not enc:
        return 404, {"error": "ENCOUNTER_NOT_FOUND"}
    if enc[0]["status"] not in ("in_progress", "completed"):
        return 400, {"error": "ENCOUNTER_NOT_OPEN", "detail": f"status={enc[0]['status']}"}

    t = _lookup_type(db, type_code)
    if not t:
        return 400, {"error": "INVALID_TYPE"}
    u = _lookup_unit(db, unit_code)
    if not u:
        return 400, {"error": "INVALID_UNIT"}

    is_abn = _is_abnormal(value_numeric, t["normal_range_low"], t["normal_range_high"])

    ok = db.execute_query(
        "INSERT INTO clinical_measurements "
        "(encounter_id, patient_id, type_id, unit_id, value_numeric, value_text, "
        "recorded_by, recorded_at, is_abnormal, notes) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s)",
        (
            encounter_id,
            enc[0]["patient_id"],
            t["type_id"],
            u["unit_id"],
            value_numeric,
            value_text,
            g.user_id,
            is_abn,
            notes,
        ),
    )
    if not ok:
        return 500, {"error": "DB_INSERT_FAILED"}

    new_id = db.cursor.lastrowid
    _write_audit(db, "INSERT", new_id, None, {
        "type_code": type_code, "unit_code": unit_code,
        "value_numeric": str(value_numeric) if value_numeric is not None else None,
        "value_text": value_text,
    })
    return 201, {
        "measurement_id": new_id,
        "is_abnormal": is_abn,
        "recorded_at": datetime.utcnow().isoformat() + "Z",
    }


# ----------------------------------------------------------------------
# C.7.1 — record a measurement
# ----------------------------------------------------------------------
@measurements_bp.post("/encounters/<int:encounter_id>/measurements")
@require_role("doctor", "nurse", "lab_tech", "admin")
def record_measurement(encounter_id: int):
    body = request.get_json(silent=True) or {}
    with DatabaseConnection() as db:
        status, payload = _persist_measurement(db, encounter_id, body)
    return jsonify(payload), status


# ----------------------------------------------------------------------
# C.7.2 — bulk record (vitals panel)
# ----------------------------------------------------------------------
@measurements_bp.post("/encounters/<int:encounter_id>/measurements:bulk")
@require_role("doctor", "nurse", "lab_tech", "admin")
def bulk_record(encounter_id: int):
    body = request.get_json(silent=True) or {}
    items = body.get("measurements") or []
    if not isinstance(items, list) or not items:
        return jsonify(error="EMPTY_BATCH"), 400

    created, failed = [], []
    with DatabaseConnection() as db:
        for idx, m in enumerate(items):
            status, payload = _persist_measurement(db, encounter_id, m)
            if status == 201:
                created.append(payload["measurement_id"])
            else:
                failed.append({"index": idx, "error": payload.get("error"), "detail": payload.get("detail")})
    return jsonify(created=created, failed=failed), 201


# ----------------------------------------------------------------------
# C.7.3 — retrieve patient timeline
# ----------------------------------------------------------------------
@measurements_bp.get("/patients/<int:patient_id>/measurements")
@require_role("doctor", "nurse", "lab_tech", "admin")
def patient_timeline(patient_id: int):
    type_code = request.args.get("type_code")
    date_from = request.args.get("from")
    date_to = request.args.get("to")
    limit = min(int(request.args.get("limit", 50)), 500)
    offset = max(int(request.args.get("offset", 0)), 0)

    where, params = ["cm.patient_id=%s"], [patient_id]
    if type_code:
        where.append("t.type_code=%s")
        params.append(type_code)
    if date_from:
        where.append("cm.recorded_at >= %s")
        params.append(date_from)
    if date_to:
        where.append("cm.recorded_at <= %s")
        params.append(date_to)
    where_sql = " AND ".join(where)

    with DatabaseConnection() as db:
        total_rows = db.execute_select(
            f"SELECT COUNT(*) AS n FROM clinical_measurements cm "
            f"JOIN measurement_types t ON t.type_id = cm.type_id WHERE {where_sql}",
            tuple(params),
        )
        total = total_rows[0]["n"] if total_rows else 0

        rows = db.execute_select(
            f"SELECT cm.measurement_id, cm.encounter_id, t.type_code, t.type_name, "
            f"       u.unit_code, cm.value_numeric, cm.value_text, "
            f"       cm.is_abnormal, cm.recorded_at, cm.notes "
            f"FROM clinical_measurements cm "
            f"JOIN measurement_types t ON t.type_id = cm.type_id "
            f"JOIN measurement_units u ON u.unit_id = cm.unit_id "
            f"WHERE {where_sql} "
            f"ORDER BY cm.recorded_at DESC LIMIT %s OFFSET %s",
            tuple(params + [limit, offset]),
        ) or []

    return jsonify(items=rows, total=total, limit=limit, offset=offset)


# ----------------------------------------------------------------------
# C.7.4 — update / correct
# ----------------------------------------------------------------------
@measurements_bp.patch("/measurements/<int:measurement_id>")
@require_role("doctor", "nurse", "lab_tech", "admin")
def patch_measurement(measurement_id: int):
    body = request.get_json(silent=True) or {}
    if not any(k in body for k in ("value_numeric", "value_text", "notes")):
        return jsonify(error="NO_FIELDS_TO_UPDATE"), 400

    with DatabaseConnection() as db:
        existing = db.execute_select(
            "SELECT cm.*, t.normal_range_low, t.normal_range_high "
            "FROM clinical_measurements cm JOIN measurement_types t ON t.type_id=cm.type_id "
            "WHERE cm.measurement_id=%s",
            (measurement_id,),
        )
        if not existing:
            return jsonify(error="MEASUREMENT_NOT_FOUND"), 404
        cur = existing[0]

        # CM-07: edit window
        age = datetime.utcnow() - cur["recorded_at"]
        if age > timedelta(hours=EDIT_WINDOW_HOURS) and g.role != "admin":
            return jsonify(error="EDIT_WINDOW_EXPIRED"), 403

        new_numeric = body.get("value_numeric", cur["value_numeric"])
        new_text = body.get("value_text", cur["value_text"])
        new_notes = body.get("notes", cur["notes"])
        if new_numeric is not None:
            try:
                new_numeric = Decimal(str(new_numeric))
            except InvalidOperation:
                return jsonify(error="MEASUREMENT_VALUE_REQUIRED"), 400

        is_abn = _is_abnormal(new_numeric, cur["normal_range_low"], cur["normal_range_high"])

        ok = db.execute_query(
            "UPDATE clinical_measurements SET value_numeric=%s, value_text=%s, "
            "notes=%s, is_abnormal=%s WHERE measurement_id=%s",
            (new_numeric, new_text, new_notes, is_abn, measurement_id),
        )
        if not ok:
            return jsonify(error="DB_UPDATE_FAILED"), 500

        _write_audit(
            db, "UPDATE", measurement_id,
            {"value_numeric": str(cur["value_numeric"]), "value_text": cur["value_text"], "notes": cur["notes"]},
            {"value_numeric": str(new_numeric) if new_numeric is not None else None,
             "value_text": new_text, "notes": new_notes},
        )

    return jsonify(measurement_id=measurement_id, is_abnormal=is_abn, updated=True)

"""
Exports API (v1) — C.7.5 of Requirement.md
==========================================
    GET /api/v1/exports/measurements
        ?patient_id=<int>&format=csv|xlsx|pdf&from=...&to=...

Scaffolding: CSV implemented inline; xlsx/pdf return 501 NOT_IMPLEMENTED.
Per CM-08, >1000 rows requires admin or billing.
"""

import csv
import io
import json
from datetime import datetime

from flask import Blueprint, request, jsonify, g, Response

from database_connection import DatabaseConnection
from api.auth import require_role


exports_bp = Blueprint("exports", __name__, url_prefix="/api/v1")

BULK_THRESHOLD = 1000


def _audit_export(db, row_count: int, fmt: str, params: dict):
    db.execute_query(
        "INSERT INTO audit_logs (table_name, record_id, action, user_id, user_type, "
        "new_values, ip_address, user_agent) "
        "VALUES (%s, %s, 'VIEW', %s, %s, %s, %s, %s)",
        (
            "clinical_measurements",
            0,
            g.user_id,
            g.role,
            json.dumps({"export_format": fmt, "row_count": row_count, "params": params}),
            request.remote_addr,
            request.headers.get("User-Agent", "")[:500],
        ),
    )


@exports_bp.get("/exports/measurements")
@require_role("doctor", "nurse", "lab_tech", "admin", "billing")
def export_measurements():
    patient_id = request.args.get("patient_id", type=int)
    fmt = (request.args.get("format") or "csv").lower()
    date_from = request.args.get("from")
    date_to = request.args.get("to")

    if patient_id is None:
        return jsonify(error="patient_id required"), 400
    if fmt not in ("csv", "xlsx", "pdf"):
        return jsonify(error="UNSUPPORTED_FORMAT"), 400
    if fmt in ("xlsx", "pdf"):
        return jsonify(error="NOT_IMPLEMENTED", detail=f"{fmt} export pending"), 501

    where, params = ["cm.patient_id=%s"], [patient_id]
    if date_from:
        where.append("cm.recorded_at >= %s")
        params.append(date_from)
    if date_to:
        where.append("cm.recorded_at <= %s")
        params.append(date_to)
    where_sql = " AND ".join(where)

    with DatabaseConnection() as db:
        rows = db.execute_select(
            f"SELECT cm.measurement_id, cm.encounter_id, t.type_code, t.type_name, "
            f"       u.unit_code, cm.value_numeric, cm.value_text, cm.is_abnormal, "
            f"       cm.recorded_at, cm.recorded_by, cm.notes "
            f"FROM clinical_measurements cm "
            f"JOIN measurement_types t ON t.type_id = cm.type_id "
            f"JOIN measurement_units u ON u.unit_id = cm.unit_id "
            f"WHERE {where_sql} ORDER BY cm.recorded_at DESC",
            tuple(params),
        ) or []

        if len(rows) > BULK_THRESHOLD and g.role not in ("admin", "billing"):
            return jsonify(error="BULK_EXPORT_FORBIDDEN", row_count=len(rows)), 403

        # CSV build
        buf = io.StringIO()
        writer = csv.writer(buf)
        if rows:
            writer.writerow(rows[0].keys())
            for r in rows:
                writer.writerow([r[k] for k in rows[0].keys()])
        body = buf.getvalue()

        _audit_export(db, len(rows), fmt, {"patient_id": patient_id, "from": date_from, "to": date_to})

    filename = f"measurements_p{patient_id}_{datetime.utcnow():%Y%m%d_%H%M%S}.csv"
    return Response(
        body,
        mimetype="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

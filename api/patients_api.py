"""
Patients API (v1)
=================
    GET  /api/v1/patients              — list (with limit/offset)
    POST /api/v1/patients              — create
    GET  /api/v1/patients/<id>         — single fetch

Scaffolding: writes audit_logs row on create. MRN uniqueness enforced
at DB level; we surface 409 on conflict.
"""

import json
from datetime import date, datetime

from flask import Blueprint, request, jsonify, g

from database_connection import DatabaseConnection
from api.auth import require_role


patients_bp = Blueprint("patients", __name__, url_prefix="/api/v1")

REQUIRED_FIELDS = ("mrn", "first_name", "last_name", "date_of_birth", "gender")
ALLOWED_GENDERS = {"Male", "Female", "Other", "Prefer not to say"}


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def _row_to_patient(r: dict) -> dict:
    """Reshape a DB row into the UI-friendly Patient shape."""
    dob = r.get("date_of_birth")
    age = None
    if dob:
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    sex_map = {"Male": "M", "Female": "F", "Other": "Other", "Prefer not to say": "Other"}
    return {
        "id":     r["patient_id"],
        "mrn":    r["mrn"],
        "first":  r["first_name"],
        "last":   r["last_name"],
        "dob":    dob.isoformat() if dob else None,
        "age":    age,
        "sex":    sex_map.get(r.get("gender"), "Other"),
        "blood":  r.get("blood_group"),
        "phone":  r.get("phone"),
        "ins":    None,                     # filled by future join
        "pcp":    None,                     # filled by future join
        "status": r.get("status") or "active",
    }


def _write_audit(db, action: str, record_id: int, new_values: dict | None):
    db.execute_query(
        "INSERT INTO audit_logs (table_name, record_id, action, user_id, user_type, "
        "new_values, ip_address, user_agent) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (
            "patients",
            record_id,
            action,
            getattr(g, "user_id", None),
            getattr(g, "role", None),
            json.dumps(new_values, default=str) if new_values else None,
            request.remote_addr,
            request.headers.get("User-Agent", "")[:500],
        ),
    )


# ----------------------------------------------------------------------
# GET /api/v1/patients
# ----------------------------------------------------------------------
@patients_bp.get("/patients")
@require_role("doctor", "nurse", "lab_tech", "admin", "billing")
def list_patients():
    limit = min(int(request.args.get("limit", 50)), 500)
    offset = max(int(request.args.get("offset", 0)), 0)
    status = request.args.get("status")

    where, params = ["1=1"], []
    if status:
        where.append("status = %s")
        params.append(status)
    where_sql = " AND ".join(where)

    with DatabaseConnection() as db:
        total_rows = db.execute_select(
            f"SELECT COUNT(*) AS n FROM patients WHERE {where_sql}", tuple(params)
        )
        total = total_rows[0]["n"] if total_rows else 0

        rows = db.execute_select(
            f"SELECT patient_id, mrn, first_name, last_name, date_of_birth, "
            f"       gender, phone, blood_group, status "
            f"FROM patients WHERE {where_sql} "
            f"ORDER BY last_name, first_name LIMIT %s OFFSET %s",
            tuple(params + [limit, offset]),
        ) or []

    items = [_row_to_patient(r) for r in rows]
    return jsonify(items=items, total=total, limit=limit, offset=offset)


# ----------------------------------------------------------------------
# GET /api/v1/patients/<id>
# ----------------------------------------------------------------------
@patients_bp.get("/patients/<int:patient_id>")
@require_role("doctor", "nurse", "lab_tech", "admin", "billing")
def get_one_patient(patient_id: int):
    with DatabaseConnection() as db:
        rows = db.execute_select(
            "SELECT patient_id, mrn, first_name, last_name, date_of_birth, "
            "       gender, phone, blood_group, status "
            "FROM patients WHERE patient_id = %s",
            (patient_id,),
        )
    if not rows:
        return jsonify(error="PATIENT_NOT_FOUND"), 404
    return jsonify(_row_to_patient(rows[0]))


# ----------------------------------------------------------------------
# POST /api/v1/patients
# ----------------------------------------------------------------------
@patients_bp.post("/patients")
@require_role("doctor", "nurse", "admin")
def create_patient():
    body = request.get_json(silent=True) or {}

    # validation
    missing = [f for f in REQUIRED_FIELDS if not body.get(f)]
    if missing:
        return jsonify(error="MISSING_FIELDS", fields=missing), 400

    gender = body["gender"]
    if gender not in ALLOWED_GENDERS:
        return jsonify(error="INVALID_GENDER", allowed=sorted(ALLOWED_GENDERS)), 400

    try:
        dob = datetime.fromisoformat(body["date_of_birth"]).date()
    except ValueError:
        return jsonify(error="INVALID_DOB", detail="expected YYYY-MM-DD"), 400
    if dob > date.today():
        return jsonify(error="INVALID_DOB", detail="date_of_birth in future"), 400

    with DatabaseConnection() as db:
        # uniqueness pre-check (race condition still handled by DB constraint below)
        dupe = db.execute_select(
            "SELECT patient_id FROM patients WHERE mrn = %s LIMIT 1", (body["mrn"],)
        )
        if dupe:
            return jsonify(error="MRN_CONFLICT"), 409

        ok = db.execute_query(
            "INSERT INTO patients (mrn, first_name, middle_name, last_name, date_of_birth, "
            "                      gender, phone, email, blood_group, status) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                body["mrn"],
                body["first_name"],
                body.get("middle_name"),
                body["last_name"],
                dob,
                gender,
                body.get("phone"),
                body.get("email"),
                body.get("blood_group"),
                body.get("status", "active"),
            ),
        )
        if not ok:
            return jsonify(error="DB_INSERT_FAILED"), 500

        new_id = db.cursor.lastrowid
        _write_audit(db, "INSERT", new_id, {
            "mrn": body["mrn"],
            "name": f"{body['first_name']} {body['last_name']}",
            "dob": dob.isoformat(),
        })

        rows = db.execute_select(
            "SELECT patient_id, mrn, first_name, last_name, date_of_birth, "
            "       gender, phone, blood_group, status "
            "FROM patients WHERE patient_id = %s",
            (new_id,),
        )

    return jsonify(_row_to_patient(rows[0])), 201

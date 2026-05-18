"""
Global Search API (v1) — C.7.6 of Requirement.md
================================================
    GET /api/v1/search?q=<query>&scope=patients|encounters|measurements&limit=20

Scaffolding: simple LIKE-based search over patients (MRN, last name,
first name). encounters & measurements scopes are stubbed.
"""

from flask import Blueprint, request, jsonify

from database_connection import DatabaseConnection
from api.auth import require_role


search_bp = Blueprint("search", __name__, url_prefix="/api/v1")

VALID_SCOPES = {"patients", "encounters", "measurements"}


@search_bp.get("/search")
@require_role("doctor", "nurse", "lab_tech", "admin", "billing")
def global_search():
    q = (request.args.get("q") or "").strip()
    scope = (request.args.get("scope") or "patients").lower()
    limit = min(int(request.args.get("limit", 20)), 100)

    if not q:
        return jsonify(error="q required"), 400
    if scope not in VALID_SCOPES:
        return jsonify(error="INVALID_SCOPE", allowed=list(VALID_SCOPES)), 400

    results = []
    with DatabaseConnection() as db:
        if scope == "patients":
            like = f"%{q}%"
            rows = db.execute_select(
                "SELECT patient_id, mrn, first_name, last_name, date_of_birth "
                "FROM patients "
                "WHERE mrn LIKE %s OR last_name LIKE %s OR first_name LIKE %s "
                "ORDER BY last_name, first_name LIMIT %s",
                (like, like, like, limit),
            ) or []
            results = [
                {
                    "type": "patient",
                    "id": r["patient_id"],
                    "label": f"{r['last_name']}, {r['first_name']} ({r['mrn']})",
                    "snippet": f"DOB {r['date_of_birth']}",
                    "url": f"/api/v1/patients/{r['patient_id']}",
                }
                for r in rows
            ]
        elif scope in ("encounters", "measurements"):
            # stub — production would search encounter_number / measurement notes
            results = []

    return jsonify(results=results, query=q, scope=scope)

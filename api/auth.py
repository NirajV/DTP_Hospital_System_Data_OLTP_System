"""
Auth & RBAC stubs
=================
Production should replace this with JWT verification and a real RBAC
lookup. For scaffolding we accept two headers:

    X-User-Id:   integer user_id from `users` table
    X-User-Role: one of doctor | nurse | lab_tech | admin | billing

The @require_role decorator enforces the permissions matrix from
Requirement.md Appendix C.8.2.
"""

from functools import wraps
from flask import request, jsonify, g


VALID_ROLES = {"doctor", "nurse", "lab_tech", "admin", "billing"}


def _identify():
    user_id = request.headers.get("X-User-Id")
    role = request.headers.get("X-User-Role")
    if not user_id or not role:
        return None, None, ("MISSING_AUTH_HEADERS", 401)
    if role not in VALID_ROLES:
        return None, None, ("INVALID_ROLE", 403)
    try:
        return int(user_id), role, None
    except ValueError:
        return None, None, ("INVALID_USER_ID", 401)


def require_role(*allowed_roles: str):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            user_id, role, err = _identify()
            if err:
                code, status = err
                return jsonify(error=code), status
            if role not in allowed_roles:
                return jsonify(error="FORBIDDEN", required_roles=list(allowed_roles)), 403
            g.user_id, g.role = user_id, role
            return view(*args, **kwargs)
        return wrapper
    return decorator

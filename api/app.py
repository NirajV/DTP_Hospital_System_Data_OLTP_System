"""
Hospital OLTP — Flask API entrypoint
====================================
Wires the v1 blueprints. This is scaffolding for Appendix C.7 of
Requirement.md; auth/RBAC are stubbed via a simple header check
(see api.auth).

Run:
    pip install flask
    python -m api.app
"""

from flask import Flask, jsonify

from api.measurements_api import measurements_bp
from api.exports_api import exports_bp
from api.search_api import search_bp
from api.patients_api import patients_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(measurements_bp)
    app.register_blueprint(exports_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(patients_bp)

    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok")

    @app.errorhandler(404)
    def not_found(_):
        return jsonify(error="NOT_FOUND"), 404

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=8080, debug=True)

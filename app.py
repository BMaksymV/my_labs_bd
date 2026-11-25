from pathlib import Path
from typing import Any
from flask import Flask, jsonify
import yaml

from my_project import db, ma
from my_project.auth import domain
from my_project.auth.route.crud_routes import crud_bp
from my_project.auth.route.rental_route import rental_bp
from my_project.auth.route.stored_procedures_route import procedures_bp
from my_project.auth.route.user_route import user_bp
from my_project.utils.error_handlers import register_error_handlers


def create_app(config_override: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)

    if config_override is None or "SQLALCHEMY_DATABASE_URI" not in config_override:
        config_path = Path(__file__).resolve().parent / "config" / "app.yml"
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        db_config = config["db"]
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"mysql+pymysql://{db_config['user']}:{db_config['password']}"
            f"@{db_config['host']}/{db_config['database']}?charset=utf8mb4"
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.ensure_ascii = False

    if config_override:
        app.config.update(config_override)

    db.init_app(app)
    ma.init_app(app)

    register_error_handlers(app)

    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(rental_bp, url_prefix="/api")
    app.register_blueprint(crud_bp, url_prefix="/api")
    app.register_blueprint(procedures_bp, url_prefix="/api")

    @app.route("/api", methods=["GET"])
    def api_index():
        return jsonify(
            {
                "service": "FabLab REST API",
                "crud_resources": [
                    "/api/users",
                    "/api/projects",
                    "/api/labs",
                    "/api/equipment-categories",
                    "/api/equipment-statuses",
                    "/api/equipment-info",
                    "/api/equipment-kits",
                    "/api/equipment",
                    "/api/kit-items",
                    "/api/rentals",
                    "/api/repairs",
                    "/api/machine-sessions",
                    "/api/equipment-notes",
                    "/api/rentals-delete-log",
                ],
                "stored_procedures": [
                    "POST /api/procedures/projects",
                    "POST /api/procedures/kit-items/by-name",
                    "POST /api/procedures/categories/noname-batch",
                    "GET /api/procedures/machine-sessions/stats?operation=ALL|MIN|MAX|SUM|AVG",
                    "POST /api/procedures/projects/split-random",
                ],
            }
        ), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

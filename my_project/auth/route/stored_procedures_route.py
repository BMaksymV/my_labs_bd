from flask import Blueprint
from my_project.auth.controller.stored_procedures_controller import StoredProceduresController

procedures_bp = Blueprint("procedures", __name__)

procedures_bp.route("/procedures/projects", methods=["POST"])(
    StoredProceduresController.insert_project
)

procedures_bp.route("/procedures/kit-items/by-name", methods=["POST"])(
    StoredProceduresController.add_equipment_to_kit
)

procedures_bp.route("/procedures/categories/noname-batch", methods=["POST"])(
    StoredProceduresController.insert_10_noname_categories
)

procedures_bp.route("/procedures/machine-sessions/stats", methods=["GET"])(
    StoredProceduresController.get_session_duration_stats
)

procedures_bp.route("/procedures/projects/split-random", methods=["POST"])(
    StoredProceduresController.split_projects_random
)

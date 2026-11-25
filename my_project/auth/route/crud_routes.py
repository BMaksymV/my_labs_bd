from flask import Blueprint
from my_project.auth.controller.base_controller import BaseCRUDController
from my_project.auth.controller.general_controllers import (
    RelationshipController,
    category_controller,
    delete_log_controller,
    equipment_controller,
    info_controller,
    kit_controller,
    lab_controller,
    note_controller,
    project_controller,
    repair_controller,
    session_controller,
    status_controller,
)
from my_project.auth.controller.kit_item_controller import KitItemController

crud_bp = Blueprint("crud", __name__)


def _register_crud(
    bp: Blueprint,
    path: str,
    controller: BaseCRUDController,
    endpoint_prefix: str,
) -> None:
    bp.add_url_rule(
        path,
        endpoint=f"{endpoint_prefix}_get_all",
        view_func=controller.get_all,
        methods=["GET"],
    )
    bp.add_url_rule(
        f"{path}/<int:entity_id>",
        endpoint=f"{endpoint_prefix}_get_by_id",
        view_func=controller.get_by_id,
        methods=["GET"],
    )
    bp.add_url_rule(
        path,
        endpoint=f"{endpoint_prefix}_create",
        view_func=controller.create,
        methods=["POST"],
    )
    bp.add_url_rule(
        f"{path}/<int:entity_id>",
        endpoint=f"{endpoint_prefix}_update",
        view_func=controller.update,
        methods=["PUT"],
    )
    bp.add_url_rule(
        f"{path}/<int:entity_id>",
        endpoint=f"{endpoint_prefix}_delete",
        view_func=controller.delete,
        methods=["DELETE"],
    )


_register_crud(crud_bp, "/projects", project_controller, "projects")
_register_crud(crud_bp, "/labs", lab_controller, "labs")
_register_crud(crud_bp, "/equipment-categories", category_controller, "equipment_categories")
_register_crud(crud_bp, "/equipment-statuses", status_controller, "equipment_statuses")
_register_crud(crud_bp, "/equipment-info", info_controller, "equipment_info")
_register_crud(crud_bp, "/equipment-kits", kit_controller, "equipment_kits")
_register_crud(crud_bp, "/equipment", equipment_controller, "equipment")
_register_crud(crud_bp, "/repairs", repair_controller, "repairs")
_register_crud(crud_bp, "/machine-sessions", session_controller, "machine_sessions")
_register_crud(crud_bp, "/equipment-notes", note_controller, "equipment_notes")
_register_crud(crud_bp, "/rentals-delete-log", delete_log_controller, "rentals_delete_log")

crud_bp.route("/kit-items", methods=["GET"])(KitItemController.get_all)
crud_bp.route("/kit-items/<int:equipment_id>/<int:kit_id>", methods=["GET"])(
    KitItemController.get_by_ids
)
crud_bp.route("/kit-items", methods=["POST"])(KitItemController.create)
crud_bp.route("/kit-items/<int:equipment_id>/<int:kit_id>", methods=["PUT"])(
    KitItemController.update
)
crud_bp.route("/kit-items/<int:equipment_id>/<int:kit_id>", methods=["DELETE"])(
    KitItemController.delete
)

crud_bp.route("/projects/<int:project_id>/rentals", methods=["GET"])(
    RelationshipController.get_project_rentals
)
crud_bp.route("/labs/<int:lab_id>/rentals", methods=["GET"])(
    RelationshipController.get_lab_rentals
)
crud_bp.route("/equipment-categories/<int:category_id>/equipment", methods=["GET"])(
    RelationshipController.get_category_equipment
)
crud_bp.route("/equipment-statuses/<int:status_id>/equipment", methods=["GET"])(
    RelationshipController.get_status_equipment
)
crud_bp.route("/equipment-kits/<int:kit_id>/equipment", methods=["GET"])(
    RelationshipController.get_kit_equipment
)
crud_bp.route("/equipment/<int:equipment_id>/kits", methods=["GET"])(
    RelationshipController.get_equipment_kits
)
crud_bp.route("/equipment/<int:equipment_id>/notes", methods=["GET"])(
    RelationshipController.get_equipment_notes
)
crud_bp.route("/equipment/<int:equipment_id>/repairs", methods=["GET"])(
    RelationshipController.get_equipment_repairs
)
crud_bp.route("/equipment/<int:equipment_id>/rentals", methods=["GET"])(
    RelationshipController.get_equipment_rentals
)

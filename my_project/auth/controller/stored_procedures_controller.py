from flask import jsonify, request
from my_project.auth.controller.base_controller import get_json_body
from my_project.auth.service.stored_procedures_service import StoredProceduresService

procedures_service = StoredProceduresService()


class StoredProceduresController:
    @staticmethod
    def insert_project():
        data = get_json_body()
        created = procedures_service.insert_project(data)
        return jsonify(created), 201

    @staticmethod
    def add_equipment_to_kit():
        data = get_json_body()
        result = procedures_service.add_equipment_to_kit(data)
        return jsonify(result), 201

    @staticmethod
    def insert_10_noname_categories():
        data = get_json_body(allow_empty=True)
        inserted = procedures_service.insert_10_noname_categories(data)
        return jsonify({"inserted_count": len(inserted), "items": inserted}), 201

    @staticmethod
    def get_session_duration_stats():
        operation = request.args.get("operation", "ALL")
        stats = procedures_service.get_session_duration_stats(operation)
        return jsonify(stats), 200

    @staticmethod
    def split_projects_random():
        result = procedures_service.split_projects_random()
        return jsonify(result), 201

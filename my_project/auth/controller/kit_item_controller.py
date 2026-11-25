from flask import jsonify
from my_project.auth.controller.base_controller import get_json_body
from my_project.auth.domain.schemas import KitItemDTO
from my_project.auth.service.kit_item_service import KitItemService

kit_item_service = KitItemService()
kit_item_dto = KitItemDTO()
kit_items_dto = KitItemDTO(many=True)


class KitItemController:
    @staticmethod
    def get_all():
        items = kit_item_service.get_all()
        return jsonify(kit_items_dto.dump(items)), 200

    @staticmethod
    def get_by_ids(equipment_id: int, kit_id: int):
        item = kit_item_service.get_by_ids(equipment_id, kit_id)
        return jsonify(kit_item_dto.dump(item)), 200

    @staticmethod
    def create():
        data = get_json_body()
        item = kit_item_service.create(data)
        return jsonify(kit_item_dto.dump(item)), 201

    @staticmethod
    def update(equipment_id: int, kit_id: int):
        data = get_json_body()
        item = kit_item_service.update(equipment_id, kit_id, data)
        return jsonify(kit_item_dto.dump(item)), 200

    @staticmethod
    def delete(equipment_id: int, kit_id: int):
        kit_item_service.delete(equipment_id, kit_id)
        return "", 204

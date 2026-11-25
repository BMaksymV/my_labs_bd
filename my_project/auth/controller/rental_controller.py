from flask import jsonify
from my_project.auth.controller.base_controller import get_json_body
from my_project.auth.domain.schemas import EquipmentDTO, RentalDTO
from my_project.auth.service.general_services import RentalService

rental_service = RentalService()
rental_dto = RentalDTO()
rentals_dto = RentalDTO(many=True)
equipment_dto = EquipmentDTO()


class RentalController:
    @staticmethod
    def get_all():
        rentals = rental_service.get_all()
        return jsonify(rentals_dto.dump(rentals)), 200

    @staticmethod
    def get_by_id(rental_id: int):
        rental = rental_service.get_by_id(rental_id)
        return jsonify(rental_dto.dump(rental)), 200

    @staticmethod
    def create():
        data = get_json_body()
        rental = rental_service.create(data)
        return jsonify(rental_dto.dump(rental)), 201

    @staticmethod
    def update(rental_id: int):
        data = get_json_body()
        rental = rental_service.update(rental_id, data)
        return jsonify(rental_dto.dump(rental)), 200

    @staticmethod
    def delete(rental_id: int):
        rental_service.delete(rental_id)
        return "", 204

    @staticmethod
    def get_rental_equipment(rental_id: int):
        rental = rental_service.get_by_id(rental_id)
        return jsonify(equipment_dto.dump(rental.equipment)), 200

from flask import jsonify
from my_project.auth.controller.base_controller import get_json_body
from my_project.auth.domain.schemas import MachineSessionDTO, RentalDTO, UserDTO
from my_project.auth.service.user_service import UserService

user_service = UserService()
user_dto = UserDTO()
users_dto = UserDTO(many=True)
rentals_dto = RentalDTO(many=True)
sessions_dto = MachineSessionDTO(many=True)


class UserController:
    @staticmethod
    def get_all():
        users = user_service.get_all_users()
        return jsonify(users_dto.dump(users)), 200

    @staticmethod
    def get_by_id(user_id: int):
        user = user_service.get_user_by_id(user_id)
        return jsonify(user_dto.dump(user)), 200

    @staticmethod
    def create():
        data = get_json_body()
        user = user_service.create_user(data)
        return jsonify(user_dto.dump(user)), 201

    @staticmethod
    def update(user_id: int):
        data = get_json_body()
        user = user_service.update_user(user_id, data)
        return jsonify(user_dto.dump(user)), 200

    @staticmethod
    def delete(user_id: int):
        user_service.delete_user(user_id)
        return "", 204

    @staticmethod
    def get_user_rentals(user_id: int):
        user = user_service.get_user_by_id(user_id)
        return jsonify(rentals_dto.dump(user.rentals)), 200

    @staticmethod
    def get_user_sessions(user_id: int):
        user = user_service.get_user_by_id(user_id)
        return jsonify(sessions_dto.dump(user.machine_sessions)), 200

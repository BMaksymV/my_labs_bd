from flask import request, jsonify
from my_project.auth.service.user_service import UserService
from my_project.auth.domain.schemas import UserDTO
from my_project.auth.domain.schemas import (
    UserDTO,
    RentalDTO,
    EquipmentDTO
)

user_service = UserService()
user_dto = UserDTO()
users_dto = UserDTO(many=True)

class UserController:
    @staticmethod
    def get_all():
        users = user_service.get_all_users()
        return jsonify(users_dto.dump(users)), 200

    @staticmethod
    def get_by_id(user_id):
        user = user_service.get_user_by_id(user_id)
        if user:
            return jsonify(user_dto.dump(user)), 200
        return jsonify({"message": "User not found"}), 404

    @staticmethod
    def create():
        data = request.get_json()
        user = user_service.create_user(data)
        return jsonify(user_dto.dump(user)), 201

    @staticmethod
    def update(user_id):
        data = request.get_json()
        user = user_service.update_user(user_id, data)
        if user:
            return jsonify(user_dto.dump(user)), 200
        return jsonify({"message": "User not found"}), 404

    @staticmethod
    def delete(user_id):
        success = user_service.delete_user(user_id)
        if success:
            return '', 204
        return jsonify({"message": "User not found"}), 404
        
    @staticmethod
    def get_user_rentals(user_id):
        # Реалізація вимоги зв'язку M:1
        user = user_service.get_user_by_id(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        # Передбачається наявність RentalDTO
        # return jsonify(rentals_dto.dump(user.rentals)), 200
        return jsonify({"user": user.first_name, "rentals_count": len(user.rentals)}), 200
    
    @staticmethod
    def get_user_rentals(user_id):
        user = user_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'Користувача не знайдено'}), 404
        
        # Витягуємо всі оренди цього юзера (зв'язок 1:M)
        rentals_dto = RentalDTO(many=True)
        return jsonify(rentals_dto.dump(user.rentals)), 200
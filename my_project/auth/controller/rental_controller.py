from flask import jsonify
from my_project.auth.domain.rental import Rental
from my_project.auth.domain.equipment import EquipmentDTO

class RentalController:
    @staticmethod
    def get_rental_equipment(rental_id):
        rental = Rental.query.get(rental_id)
        if not rental:
            return jsonify({'error': 'Оренду не знайдено'}), 404
        
        # Витягуємо обладнання зі стикувальної таблиці (зв'язок M:M)
        equipment_dto = EquipmentDTO(many=True)
        return jsonify(equipment_dto.dump(rental.equipment_list)), 200
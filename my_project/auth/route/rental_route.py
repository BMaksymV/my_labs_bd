from flask import Blueprint
from my_project.auth.controller.rental_controller import RentalController

rental_bp = Blueprint('rental_bp', __name__)

rental_bp.route('/rentals/<int:rental_id>/equipment', methods=['GET'])(RentalController.get_rental_equipment)
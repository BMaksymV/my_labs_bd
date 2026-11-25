from flask import Blueprint
from my_project.auth.controller.rental_controller import RentalController

rental_bp = Blueprint("rentals", __name__)

rental_bp.route("/rentals", methods=["GET"])(RentalController.get_all)
rental_bp.route("/rentals/<int:rental_id>", methods=["GET"])(RentalController.get_by_id)
rental_bp.route("/rentals", methods=["POST"])(RentalController.create)
rental_bp.route("/rentals/<int:rental_id>", methods=["PUT"])(RentalController.update)
rental_bp.route("/rentals/<int:rental_id>", methods=["DELETE"])(RentalController.delete)

rental_bp.route("/rentals/<int:rental_id>/equipment", methods=["GET"])(
    RentalController.get_rental_equipment
)

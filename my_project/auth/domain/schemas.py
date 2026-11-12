from my_project import ma

from .user import User
from .rental import Rental
from .equipment import Equipment


class UserDTO(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


class RentalDTO(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rental
        load_instance = True
        include_fk = True


class EquipmentDTO(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Equipment
        load_instance = True
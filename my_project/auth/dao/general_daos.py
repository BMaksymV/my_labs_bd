from my_project import db
from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain import (
    Equipment,
    EquipmentCategory,
    EquipmentInfo,
    EquipmentKit,
    EquipmentNote,
    EquipmentStatus,
    Lab,
    MachineSession,
    Project,
    Rental,
    RentalsDeleteLog,
    Repair,
)


class ProjectDAO(BaseDAO[Project]):
    def __init__(self) -> None:
        super().__init__(Project)


class LabDAO(BaseDAO[Lab]):
    def __init__(self) -> None:
        super().__init__(Lab)


class EquipmentCategoryDAO(BaseDAO[EquipmentCategory]):
    def __init__(self) -> None:
        super().__init__(EquipmentCategory)


class EquipmentStatusDAO(BaseDAO[EquipmentStatus]):
    def __init__(self) -> None:
        super().__init__(EquipmentStatus)


class EquipmentInfoDAO(BaseDAO[EquipmentInfo]):
    def __init__(self) -> None:
        super().__init__(EquipmentInfo)


class EquipmentKitDAO(BaseDAO[EquipmentKit]):
    def __init__(self) -> None:
        super().__init__(EquipmentKit)


class EquipmentDAO(BaseDAO[Equipment]):
    def __init__(self) -> None:
        super().__init__(Equipment)


class RentalDAO(BaseDAO[Rental]):
    def __init__(self) -> None:
        super().__init__(Rental)


class RepairDAO(BaseDAO[Repair]):
    def __init__(self) -> None:
        super().__init__(Repair)


class MachineSessionDAO(BaseDAO[MachineSession]):
    def __init__(self) -> None:
        super().__init__(MachineSession)


class EquipmentNoteDAO(BaseDAO[EquipmentNote]):
    def __init__(self) -> None:
        super().__init__(EquipmentNote)

    def find_by_equipment_id(self, equipment_id: int) -> list[EquipmentNote]:
        return (
            db.session.query(EquipmentNote)
            .filter(EquipmentNote.equipment_id == equipment_id)
            .all()
        )


class RentalsDeleteLogDAO(BaseDAO[RentalsDeleteLog]):
    def __init__(self) -> None:
        super().__init__(RentalsDeleteLog)

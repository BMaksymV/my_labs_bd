from typing import Any
from my_project.auth.dao.general_daos import (
    EquipmentCategoryDAO,
    EquipmentDAO,
    EquipmentInfoDAO,
    EquipmentKitDAO,
    EquipmentNoteDAO,
    EquipmentStatusDAO,
    LabDAO,
    MachineSessionDAO,
    ProjectDAO,
    RentalDAO,
    RentalsDeleteLogDAO,
    RepairDAO,
)
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
from my_project.auth.domain.schemas import (
    EquipmentCategoryDTO,
    EquipmentDTO,
    EquipmentInfoDTO,
    EquipmentKitDTO,
    EquipmentNoteDTO,
    EquipmentStatusDTO,
    LabDTO,
    MachineSessionDTO,
    ProjectDTO,
    RentalDTO,
    RentalsDeleteLogDTO,
    RepairDTO,
)
from my_project.auth.service.base_service import BaseService
from my_project.utils.exceptions import ValidationError


class ProjectService(BaseService[Project]):
    def __init__(self) -> None:
        super().__init__(dao=ProjectDAO(), schema=ProjectDTO(), entity_name="Project")


class LabService(BaseService[Lab]):
    def __init__(self) -> None:
        super().__init__(dao=LabDAO(), schema=LabDTO(), entity_name="Lab")


class EquipmentCategoryService(BaseService[EquipmentCategory]):
    def __init__(self) -> None:
        super().__init__(
            dao=EquipmentCategoryDAO(),
            schema=EquipmentCategoryDTO(),
            entity_name="EquipmentCategory",
        )


class EquipmentStatusService(BaseService[EquipmentStatus]):
    def __init__(self) -> None:
        super().__init__(
            dao=EquipmentStatusDAO(),
            schema=EquipmentStatusDTO(),
            entity_name="EquipmentStatus",
        )


class EquipmentInfoService(BaseService[EquipmentInfo]):
    def __init__(self) -> None:
        super().__init__(
            dao=EquipmentInfoDAO(),
            schema=EquipmentInfoDTO(),
            entity_name="EquipmentInfo",
        )


class EquipmentKitService(BaseService[EquipmentKit]):
    def __init__(self) -> None:
        super().__init__(
            dao=EquipmentKitDAO(),
            schema=EquipmentKitDTO(),
            entity_name="EquipmentKit",
        )


class EquipmentService(BaseService[Equipment]):
    def __init__(self) -> None:
        super().__init__(
            dao=EquipmentDAO(),
            schema=EquipmentDTO(),
            entity_name="Equipment",
        )


class RentalService(BaseService[Rental]):
    def __init__(self) -> None:
        super().__init__(dao=RentalDAO(), schema=RentalDTO(), entity_name="Rental")

    def validate_business_rules(
        self,
        data: dict[str, Any],
        existing: Rental | None = None,
    ) -> None:
        checkout_time = data.get("checkout_time", existing.checkout_time if existing else None)
        return_time = data.get("return_time", existing.return_time if existing else None)
        if checkout_time is not None and return_time is not None and return_time < checkout_time:
            raise ValidationError("return_time cannot be earlier than checkout_time")


class RepairService(BaseService[Repair]):
    def __init__(self) -> None:
        super().__init__(dao=RepairDAO(), schema=RepairDTO(), entity_name="Repair")

    def validate_business_rules(
        self,
        data: dict[str, Any],
        existing: Repair | None = None,
    ) -> None:
        start_date = data.get("start_date", existing.start_date if existing else None)
        end_date = data.get("end_date", existing.end_date if existing else None)
        if start_date is not None and end_date is not None and end_date < start_date:
            raise ValidationError("end_date cannot be earlier than start_date")


class MachineSessionService(BaseService[MachineSession]):
    def __init__(self) -> None:
        super().__init__(
            dao=MachineSessionDAO(),
            schema=MachineSessionDTO(),
            entity_name="MachineSession",
        )


class EquipmentNoteService(BaseService[EquipmentNote]):
    def __init__(self) -> None:
        super().__init__(
            dao=EquipmentNoteDAO(),
            schema=EquipmentNoteDTO(),
            entity_name="EquipmentNote",
        )

    def get_by_equipment_id(self, equipment_id: int) -> list[EquipmentNote]:
        return self.dao.find_by_equipment_id(equipment_id)


class RentalsDeleteLogService(BaseService[RentalsDeleteLog]):
    def __init__(self) -> None:
        super().__init__(
            dao=RentalsDeleteLogDAO(),
            schema=RentalsDeleteLogDTO(),
            entity_name="RentalsDeleteLog",
        )

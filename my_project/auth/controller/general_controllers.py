from flask import jsonify
from my_project.auth.controller.base_controller import BaseCRUDController
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
from my_project.auth.service.general_services import (
    EquipmentCategoryService,
    EquipmentInfoService,
    EquipmentKitService,
    EquipmentNoteService,
    EquipmentService,
    EquipmentStatusService,
    LabService,
    MachineSessionService,
    ProjectService,
    RentalsDeleteLogService,
    RepairService,
)

project_service = ProjectService()
lab_service = LabService()
category_service = EquipmentCategoryService()
status_service = EquipmentStatusService()
info_service = EquipmentInfoService()
kit_service = EquipmentKitService()
equipment_service = EquipmentService()
repair_service = RepairService()
session_service = MachineSessionService()
note_service = EquipmentNoteService()
delete_log_service = RentalsDeleteLogService()

project_controller = BaseCRUDController(project_service, ProjectDTO)
lab_controller = BaseCRUDController(lab_service, LabDTO)
category_controller = BaseCRUDController(category_service, EquipmentCategoryDTO)
status_controller = BaseCRUDController(status_service, EquipmentStatusDTO)
info_controller = BaseCRUDController(info_service, EquipmentInfoDTO)
kit_controller = BaseCRUDController(kit_service, EquipmentKitDTO)
equipment_controller = BaseCRUDController(equipment_service, EquipmentDTO)
repair_controller = BaseCRUDController(repair_service, RepairDTO)
session_controller = BaseCRUDController(session_service, MachineSessionDTO)
note_controller = BaseCRUDController(note_service, EquipmentNoteDTO)
delete_log_controller = BaseCRUDController(delete_log_service, RentalsDeleteLogDTO)

_rentals_dto = RentalDTO(many=True)
_equipment_dto = EquipmentDTO(many=True)
_kits_dto = EquipmentKitDTO(many=True)
_notes_dto = EquipmentNoteDTO(many=True)
_repairs_dto = RepairDTO(many=True)


class RelationshipController:
    @staticmethod
    def get_project_rentals(project_id: int):
        project = project_service.get_by_id(project_id)
        return jsonify(_rentals_dto.dump(project.rentals)), 200

    @staticmethod
    def get_lab_rentals(lab_id: int):
        lab = lab_service.get_by_id(lab_id)
        return jsonify(_rentals_dto.dump(lab.rentals)), 200

    @staticmethod
    def get_category_equipment(category_id: int):
        category = category_service.get_by_id(category_id)
        return jsonify(_equipment_dto.dump(category.equipment)), 200

    @staticmethod
    def get_status_equipment(status_id: int):
        status = status_service.get_by_id(status_id)
        return jsonify(_equipment_dto.dump(status.equipment)), 200

    @staticmethod
    def get_kit_equipment(kit_id: int):
        kit = kit_service.get_by_id(kit_id)
        return jsonify(_equipment_dto.dump(kit.items)), 200

    @staticmethod
    def get_equipment_kits(equipment_id: int):
        eq = equipment_service.get_by_id(equipment_id)
        return jsonify(_kits_dto.dump(eq.kits)), 200

    @staticmethod
    def get_equipment_notes(equipment_id: int):
        equipment_service.get_by_id(equipment_id)
        notes = note_service.get_by_equipment_id(equipment_id)
        return jsonify(_notes_dto.dump(notes)), 200

    @staticmethod
    def get_equipment_repairs(equipment_id: int):
        eq = equipment_service.get_by_id(equipment_id)
        return jsonify(_repairs_dto.dump(eq.repairs)), 200

    @staticmethod
    def get_equipment_rentals(equipment_id: int):
        eq = equipment_service.get_by_id(equipment_id)
        return jsonify(_rentals_dto.dump(eq.rentals)), 200

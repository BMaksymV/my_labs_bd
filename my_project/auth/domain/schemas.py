from marshmallow import RAISE, fields, validate
from my_project import ma
from my_project.auth.domain import (
    Equipment,
    EquipmentCategory,
    EquipmentInfo,
    EquipmentKit,
    EquipmentNote,
    EquipmentStatus,
    KitItem,
    Lab,
    MachineSession,
    Project,
    Rental,
    RentalsDeleteLog,
    Repair,
    User,
)


class _BaseAutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        load_instance = False
        unknown = RAISE


class UserDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    email = fields.Email(required=True, validate=validate.Length(max=100))
    phone = fields.Str(allow_none=True, validate=validate.Length(max=45))

    class Meta(_BaseAutoSchema.Meta):
        model = User


class ProjectDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(allow_none=True)

    class Meta(_BaseAutoSchema.Meta):
        model = Project


class LabDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    lab_name = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    course_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))

    class Meta(_BaseAutoSchema.Meta):
        model = Lab


class EquipmentCategoryDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=45))

    class Meta(_BaseAutoSchema.Meta):
        model = EquipmentCategory


class EquipmentStatusDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    status_name = fields.Str(required=True, validate=validate.Length(min=1, max=45))

    class Meta(_BaseAutoSchema.Meta):
        model = EquipmentStatus


class EquipmentInfoDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    instruction = fields.Str(required=True, validate=validate.Length(min=1))

    class Meta(_BaseAutoSchema.Meta):
        model = EquipmentInfo


class EquipmentKitDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    kit_name = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    description = fields.Str(allow_none=True)

    class Meta(_BaseAutoSchema.Meta):
        model = EquipmentKit


class EquipmentDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    inventory_number = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    status_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    equipment_info_id = fields.Int(allow_none=True)

    class Meta(_BaseAutoSchema.Meta):
        model = Equipment


class KitItemDTO(_BaseAutoSchema):
    equipment_id = fields.Int(required=True)
    kit_id = fields.Int(required=True)

    class Meta(_BaseAutoSchema.Meta):
        model = KitItem


class RentalDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    checkout_time = fields.DateTime(required=True)
    return_time = fields.DateTime(allow_none=True)
    user_id = fields.Int(required=True)
    equipment_id = fields.Int(required=True)
    project_id = fields.Int(allow_none=True)
    lab_id = fields.Int(allow_none=True)

    class Meta(_BaseAutoSchema.Meta):
        model = Rental


class RepairDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    issue_description = fields.Str(required=True, validate=validate.Length(min=1))
    start_date = fields.Date(required=True)
    end_date = fields.Date(allow_none=True)
    equipment_id = fields.Int(required=True)

    class Meta(_BaseAutoSchema.Meta):
        model = Repair


class MachineSessionDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    session_start = fields.DateTime(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    equipment_id = fields.Int(required=True)
    user_id = fields.Int(required=True)

    class Meta(_BaseAutoSchema.Meta):
        model = MachineSession


class EquipmentNoteDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    equipment_id = fields.Int(required=True)
    note_text = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    created_at = fields.DateTime(required=False)

    class Meta(_BaseAutoSchema.Meta):
        model = EquipmentNote


class RentalsDeleteLogDTO(_BaseAutoSchema):
    id = fields.Int(dump_only=True)
    rental_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    equipment_id = fields.Int(required=True)
    checkout_time = fields.DateTime(required=True)
    return_time = fields.DateTime(allow_none=True)
    deleted_at = fields.DateTime(required=False)

    class Meta(_BaseAutoSchema.Meta):
        model = RentalsDeleteLog

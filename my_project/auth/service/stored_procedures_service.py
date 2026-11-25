from typing import Any
from my_project.auth.dao.stored_procedures_dao import StoredProceduresDAO
from my_project.utils.exceptions import ValidationError

_ALLOWED_STAT_OPS = {"MIN", "MAX", "SUM", "AVG", "ALL"}


class StoredProceduresService:
    def __init__(self) -> None:
        self.dao = StoredProceduresDAO()

    def insert_project(self, data: dict[str, Any]) -> dict[str, Any]:
        title = data.get("title")
        description = data.get("description")
        if not isinstance(title, str) or not title.strip():
            raise ValidationError("Field 'title' must be a non-empty string")
        if len(title.strip()) > 100:
            raise ValidationError("Field 'title' cannot exceed 100 characters")
        if description is not None and not isinstance(description, str):
            raise ValidationError("Field 'description' must be a string or null")
        return self.dao.insert_project(title.strip(), description)

    def add_equipment_to_kit(self, data: dict[str, Any]) -> dict[str, Any]:
        equipment_name = data.get("equipment_name")
        kit_name = data.get("kit_name")
        if not isinstance(equipment_name, str) or not equipment_name.strip():
            raise ValidationError("Field 'equipment_name' must be a non-empty string")
        if not isinstance(kit_name, str) or not kit_name.strip():
            raise ValidationError("Field 'kit_name' must be a non-empty string")
        return self.dao.add_equipment_to_kit(equipment_name.strip(), kit_name.strip())

    def insert_10_noname_categories(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        start_num = data.get("start_num", 1)
        if isinstance(start_num, bool) or not isinstance(start_num, int) or start_num < 0:
            raise ValidationError("Field 'start_num' must be a non-negative integer")
        return self.dao.insert_10_noname_categories(start_num)

    def get_session_duration_stats(self, operation: str | None) -> dict[str, Any]:
        op = (operation or "ALL").strip().upper()
        if op not in _ALLOWED_STAT_OPS:
            raise ValidationError(
                f"Invalid operation '{operation}'. Allowed values: MIN, MAX, SUM, AVG, ALL"
            )
        return self.dao.get_session_duration_stats(op)

    def split_projects_random(self) -> dict[str, Any]:
        return self.dao.split_projects_random()

from typing import Any
from my_project.auth.dao.kit_item_dao import KitItemDAO
from my_project.auth.domain.equipment_kit import KitItem
from my_project.auth.domain.schemas import KitItemDTO
from my_project.utils.exceptions import ConflictError, NotFoundError, ValidationError


class KitItemService:
    def __init__(self) -> None:
        self.dao = KitItemDAO()
        self.schema = KitItemDTO()

    def get_all(self) -> list[KitItem]:
        return self.dao.find_all()

    def get_by_ids(self, equipment_id: int, kit_id: int) -> KitItem:
        item = self.dao.find_by_ids(equipment_id, kit_id)
        if item is None:
            raise NotFoundError(
                f"KitItem with equipment_id={equipment_id}, kit_id={kit_id} not found"
            )
        return item

    def create(self, raw_data: dict[str, Any]) -> KitItem:
        validated = self.schema.load(raw_data)
        existing = self.dao.find_by_ids(validated["equipment_id"], validated["kit_id"])
        if existing is not None:
            raise ConflictError(
                f"KitItem (equipment_id={validated['equipment_id']}, kit_id={validated['kit_id']}) already exists",
                error_code="DUPLICATE_ENTRY",
            )
        return self.dao.create(KitItem(**validated))

    def update(
        self,
        equipment_id: int,
        kit_id: int,
        raw_data: dict[str, Any],
    ) -> KitItem:
        if not raw_data:
            raise ValidationError("At least one field must be provided for update")
        item = self.get_by_ids(equipment_id, kit_id)
        validated = self.schema.load(raw_data, partial=True)
        new_equipment_id = validated.get("equipment_id", equipment_id)
        new_kit_id = validated.get("kit_id", kit_id)
        if (new_equipment_id, new_kit_id) != (equipment_id, kit_id):
            if self.dao.find_by_ids(new_equipment_id, new_kit_id) is not None:
                raise ConflictError(
                    f"KitItem (equipment_id={new_equipment_id}, kit_id={new_kit_id}) already exists",
                    error_code="DUPLICATE_ENTRY",
                )
        return self.dao.update(item, new_equipment_id, new_kit_id)

    def delete(self, equipment_id: int, kit_id: int) -> None:
        item = self.get_by_ids(equipment_id, kit_id)
        self.dao.delete(item)

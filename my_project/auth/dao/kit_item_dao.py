from my_project import db
from my_project.auth.domain.equipment_kit import KitItem


class KitItemDAO:
    def find_all(self) -> list[KitItem]:
        return db.session.query(KitItem).all()

    def find_by_ids(self, equipment_id: int, kit_id: int) -> KitItem | None:
        return db.session.get(KitItem, (equipment_id, kit_id))

    def create(self, item: KitItem) -> KitItem:
        db.session.add(item)
        db.session.commit()
        return item

    def update(self, item: KitItem, new_equipment_id: int, new_kit_id: int) -> KitItem:
        item.equipment_id = new_equipment_id
        item.kit_id = new_kit_id
        db.session.commit()
        return item

    def delete(self, item: KitItem) -> None:
        db.session.delete(item)
        db.session.commit()

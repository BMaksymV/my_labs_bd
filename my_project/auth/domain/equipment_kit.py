from my_project import db


class KitItem(db.Model):
    __tablename__ = "kit_items"

    equipment_id = db.Column(
        db.Integer,
        db.ForeignKey("equipment.id"),
        primary_key=True,
    )
    kit_id = db.Column(
        db.Integer,
        db.ForeignKey("equipment_kits.id"),
        primary_key=True,
    )


class EquipmentKit(db.Model):
    __tablename__ = "equipment_kits"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kit_name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text, nullable=True)

    items = db.relationship(
        "Equipment",
        secondary="kit_items",
        back_populates="kits",
        lazy=True,
    )

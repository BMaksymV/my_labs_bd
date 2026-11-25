from my_project import db


class Equipment(db.Model):
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    inventory_number = db.Column(db.String(45), nullable=False, unique=True)
    name = db.Column(db.String(45), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("equipment_statuses.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("equipment_categories.id"), nullable=False)
    equipment_info_id = db.Column(db.Integer, db.ForeignKey("equipment_info.id"), nullable=True)

    status = db.relationship("EquipmentStatus", back_populates="equipment")
    category = db.relationship("EquipmentCategory", back_populates="equipment")
    info = db.relationship("EquipmentInfo", back_populates="equipment")
    kits = db.relationship(
        "EquipmentKit",
        secondary="kit_items",
        back_populates="items",
        lazy=True,
    )
    rentals = db.relationship("Rental", back_populates="equipment", lazy=True)
    repairs = db.relationship("Repair", back_populates="equipment", lazy=True)
    machine_sessions = db.relationship("MachineSession", back_populates="equipment", lazy=True)

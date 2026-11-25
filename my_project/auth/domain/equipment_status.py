from my_project import db


class EquipmentStatus(db.Model):
    __tablename__ = "equipment_statuses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_name = db.Column(db.String(45), nullable=False)

    equipment = db.relationship("Equipment", back_populates="status", lazy=True)

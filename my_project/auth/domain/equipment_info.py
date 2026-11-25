from my_project import db


class EquipmentInfo(db.Model):
    __tablename__ = "equipment_info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instruction = db.Column(db.Text, nullable=False)

    equipment = db.relationship("Equipment", back_populates="info", lazy=True)

from my_project import db


class EquipmentCategory(db.Model):
    __tablename__ = "equipment_categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)

    equipment = db.relationship("Equipment", back_populates="category", lazy=True)

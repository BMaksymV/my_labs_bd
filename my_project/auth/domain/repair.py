from my_project import db


class Repair(db.Model):
    __tablename__ = "repairs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue_description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)

    equipment = db.relationship("Equipment", back_populates="repairs")

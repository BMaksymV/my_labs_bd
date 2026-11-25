from my_project import db


class Rental(db.Model):
    __tablename__ = "rentals"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    checkout_time = db.Column(db.DateTime, nullable=False)
    return_time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=True)
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.id"), nullable=True)

    user = db.relationship("User", back_populates="rentals")
    equipment = db.relationship("Equipment", back_populates="rentals")
    project = db.relationship("Project", back_populates="rentals")
    lab = db.relationship("Lab", back_populates="rentals")

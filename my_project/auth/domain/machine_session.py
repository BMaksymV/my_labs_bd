from my_project import db


class MachineSession(db.Model):
    __tablename__ = "machine_sessions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_start = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    equipment = db.relationship("Equipment", back_populates="machine_sessions")
    user = db.relationship("User", back_populates="machine_sessions")

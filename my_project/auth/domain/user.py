from my_project import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(45), nullable=True)

    rentals = db.relationship("Rental", back_populates="user", lazy=True)
    machine_sessions = db.relationship("MachineSession", back_populates="user", lazy=True)

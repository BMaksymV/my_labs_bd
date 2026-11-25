from my_project import db


class Lab(db.Model):
    __tablename__ = "labs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lab_name = db.Column(db.String(45), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)

    rentals = db.relationship("Rental", back_populates="lab", lazy=True)

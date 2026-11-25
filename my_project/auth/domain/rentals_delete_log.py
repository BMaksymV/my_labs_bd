from datetime import datetime
from my_project import db


class RentalsDeleteLog(db.Model):
    __tablename__ = "rentals_delete_log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rental_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    equipment_id = db.Column(db.Integer, nullable=False)
    checkout_time = db.Column(db.DateTime, nullable=False)
    return_time = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now().replace(microsecond=0),
    )

from datetime import datetime
from my_project import db


class EquipmentNote(db.Model):
    __tablename__ = "equipment_notes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    equipment_id = db.Column(db.Integer, nullable=False, index=True)
    note_text = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now().replace(microsecond=0),
    )

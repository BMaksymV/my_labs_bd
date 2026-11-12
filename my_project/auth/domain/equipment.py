from my_project import db, ma

rental_equipment = db.Table('rental_equipment',
    db.Column('rental_id', db.Integer, db.ForeignKey('rentals.id'), primary_key=True),
    db.Column('equipment_id', db.Integer, db.ForeignKey('equipment.id'), primary_key=True)
)

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    
    rentals = db.relationship('Rental', secondary=rental_equipment, backref='equipment_list')

class EquipmentDTO(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Equipment
        load_instance = True
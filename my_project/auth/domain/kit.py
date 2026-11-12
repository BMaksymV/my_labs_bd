from my_project import db, ma

kit_items = db.Table('kit_items',
    db.Column('equipment_id', db.Integer, db.ForeignKey('equipment.id'), primary_key=True),
    db.Column('kit_id', db.Integer, db.ForeignKey('equipment_kits.id'), primary_key=True)
)

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))

class EquipmentKit(db.Model):
    __tablename__ = 'equipment_kits'
    id = db.Column(db.Integer, primary_key=True)
    kit_name = db.Column(db.String(45))
    
    items = db.relationship('Equipment', secondary=kit_items, backref=db.backref('kits', lazy=True))

class EquipmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Equipment

class KitSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(EquipmentSchema, many=True)
    class Meta:
        model = EquipmentKit
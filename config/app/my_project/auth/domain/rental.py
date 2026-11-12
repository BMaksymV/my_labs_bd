from my_project import db, ma

class Rental(db.Model):
    __tablename__ = 'rentals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    checkout_time = db.Column(db.DateTime, nullable=False)
    return_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class RentalDTO(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rental
        load_instance = True
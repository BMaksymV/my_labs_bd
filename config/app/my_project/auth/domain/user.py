from my_project import db, ma

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(45))

    # Зв'язок 1:M (Один користувач має багато оренд)
    #   rentals = db.relationship('Rental', backref='user', lazy=True)

class UserDTO(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
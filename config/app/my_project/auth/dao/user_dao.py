from my_project.auth.domain.user import User
from my_project import db

class UserDAO:
    def find_all(self):
        return User.query.all()

    def find_by_id(self, user_id):
        return User.query.get(user_id)

    def create(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user_id, data):
        user = self.find_by_id(user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
        return user

    def delete(self, user_id):
        user = self.find_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
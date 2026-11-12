from my_project.auth.dao.user_dao import UserDAO
from my_project.auth.domain.user import User

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def get_all_users(self):
        return self.dao.find_all()

    def get_user_by_id(self, user_id):
        return self.dao.find_by_id(user_id)

    def create_user(self, data):
        new_user = User(**data)
        return self.dao.create(new_user)

    def update_user(self, user_id, data):
        return self.dao.update(user_id, data)

    def delete_user(self, user_id):
        return self.dao.delete(user_id)
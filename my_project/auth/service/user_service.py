from my_project.auth.dao.user_dao import UserDAO
from my_project.auth.domain.schemas import UserDTO
from my_project.auth.domain.user import User
from my_project.auth.service.base_service import BaseService


class UserService(BaseService[User]):
    def __init__(self) -> None:
        super().__init__(dao=UserDAO(), schema=UserDTO(), entity_name="User")

    def get_all_users(self) -> list[User]:
        return self.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        return self.get_by_id(user_id)

    def create_user(self, data: dict) -> User:
        return self.create(data)

    def update_user(self, user_id: int, data: dict) -> User:
        return self.update(user_id, data)

    def delete_user(self, user_id: int) -> None:
        self.delete(user_id)

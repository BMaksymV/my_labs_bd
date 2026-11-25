from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain.user import User


class UserDAO(BaseDAO[User]):
    def __init__(self) -> None:
        super().__init__(User)

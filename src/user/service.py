from sqlalchemy.future import Engine

from src.dao.basic import BasicDAO
from src.database.tables import users
from src.user.models import UserResponseV1


class UserService(BasicDAO):
    def __init__(self, engine: Engine, model=users, schema=UserResponseV1):
        super().__init__(engine, model, schema)

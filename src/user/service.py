from sqlalchemy.future import Engine

from src.dao.basic import BasicDAO
from src.database.tables import users
from src.user.models import UserResponseV1, UserRequestV1, UserResponseListV1


class UserService(BasicDAO):
    def __init__(
            self,
            engine: Engine,
            model=users,
            # schema=UserRequestV1,
            schema=UserResponseV1,
            schema_list=UserResponseListV1
    ):
        super().__init__(engine, model, schema, schema_list)

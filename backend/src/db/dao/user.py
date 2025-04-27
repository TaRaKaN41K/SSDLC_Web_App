from models.db import Token, User
from . import BaseDAO


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_by_name(cls, name: str):
        return await cls.get_by_parameter(name=name)

from models.db import Token, User
from . import BaseDAO


class TokenDAO(BaseDAO):
    model = Token

    @classmethod
    async def get_by_user_id(cls, user_id: int):
        return await cls.get_by_parameter(user_id=user_id)

    @classmethod
    async def delete_by_user_id(cls, user_id: int):
        return await cls.delete_by_parameter(user_id=user_id)

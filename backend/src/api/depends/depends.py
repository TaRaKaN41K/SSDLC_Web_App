from fastapi import (
    Form,
    Depends,
)


from schemas import UserSchema
from .get_auth_user_from_token_of_type import get_auth_user_from_token_of_type
from db.dao import UserDAO
from api.utils import validate_password
from exceptions.custom_exceptions import UserNoActive


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    user = await UserDAO.get_by_name(name=username)

    validate_password(password=password, hashed_password=user.password)

    return user


get_current_auth_user = get_auth_user_from_token_of_type("access")
get_current_auth_user_from_refresh = get_auth_user_from_token_of_type("refresh")


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user

    raise UserNoActive

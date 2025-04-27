from fastapi import (
    Depends,
)


from schemas import UserSchema
from db.dao import UserDAO
from .get_current_token_payload import get_current_token_payload
from .validate_token_type import validate_token_type
from exceptions.custom_exceptions import InvalidTokenError


async def get_user_by_token_sub(payload: dict) -> UserSchema:

    username: str | None = payload.get("sub")
    if not username:
        raise InvalidTokenError("No username in token sub")

    user = await UserDAO.get_by_name(name=username)

    return UserSchema(
        id=user.id,
        name=user.name,
        password=user.password,
        email=user.email,
        photo_filename=user.photo_filename,
        active=user.active,
    )


def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user(
        payload: dict = Depends(get_current_token_payload(token_type)),
    ) -> UserSchema:
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload)
    return get_auth_user

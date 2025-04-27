from fastapi import Depends
from pydantic import BaseModel

from api.depends import get_current_active_auth_user
from schemas import UserSchema


class Response(BaseModel):
    username: str
    email: str
    photo_filename: str


async def me(
    user: UserSchema = Depends(get_current_active_auth_user),
) -> Response:
    return Response(
        username=user.name,
        email=user.email,
        photo_filename=user.photo_filename,
    )

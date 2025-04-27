from fastapi import (
    HTTPException,
    Depends,
    status
)

from db.dao import UserDAO
from schemas import UserSchema
from api.depends import get_current_active_auth_user
from api.utils import delete_photo_file


async def delete_account(
        user: UserSchema = Depends(get_current_active_auth_user),
) -> UserSchema:

    deleted_user = await UserDAO.delete_by_id(instance_id=user.id)

    await delete_photo_file(photo_filename=deleted_user.photo_filename)

    return UserSchema(
        id=deleted_user.id,
        name=deleted_user.name,
        password=deleted_user.password,
        email=deleted_user.email,
        photo_filename='',
        active=deleted_user.active,
    )


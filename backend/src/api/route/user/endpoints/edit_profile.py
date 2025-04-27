from pydantic import EmailStr
from fastapi import (
    UploadFile,
    File,
    Depends,
    HTTPException,
    status
)

from db.dao import UserDAO
from api.depends import get_current_active_auth_user
from api.utils import delete_photo_file, upload_photo
from schemas import UserSchema


async def edit_profile(
        email: EmailStr | None = None,
        photo_file: UploadFile = File(None),
        user: UserSchema = Depends(get_current_active_auth_user),
) -> UserSchema:

    new_user_data = {}

    if photo_file is not None:
        await delete_photo_file(photo_filename=user.photo_filename)
        new_user_data["photo_filename"] = await upload_photo(photo_file)
    else:
        new_user_data["photo_filename"] = user.photo_filename

    if email is not None:
        new_user_data["email"] = email

    updated_user = await UserDAO.update_by_id(instance_id=user.id, **new_user_data)

    return UserSchema(
        id=updated_user.id,
        name=updated_user.name,
        password=updated_user.password,
        email=updated_user.email,
        photo_filename=updated_user.photo_filename,
        active=updated_user.active,
    )

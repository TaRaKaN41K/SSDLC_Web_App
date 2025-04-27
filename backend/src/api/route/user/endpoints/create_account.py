from fastapi import (
    HTTPException,
    File,
    UploadFile,
    status
)
from pydantic import EmailStr
from typing import Optional

from db.dao import UserDAO
from schemas import UserSchema
from api.utils import upload_photo, hash_password


async def create_account(
        username: str,
        email: EmailStr,
        password: str,
        photo_file: Optional[UploadFile] = File(None),
) -> UserSchema:

    if photo_file is not None:
        photo_filename = await upload_photo(photo_file)
    else:
        photo_filename = ""

    new_user_data = {
        "name": username,
        "email": email,
        "password": hash_password(password),
        "photo_filename": photo_filename,
        "active": False,
    }

    user = await UserDAO.add(**new_user_data)

    return UserSchema(
        id=user.id,
        name=user.name,
        password=user.password,
        email=user.email,
        photo_filename=user.photo_filename,
        active=user.active,
    )


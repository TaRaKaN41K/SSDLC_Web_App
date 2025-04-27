from fastapi import (
    Request,
    Response,
    Depends,
)
from db.dao import TokenDAO, UserDAO
from schemas import UserSchema, TokenInfo
from api.utils import (
    create_access_token,
    create_refresh_token,
    get_device_id,
)
from api.depends import validate_auth_user


async def login(
        request: Request,
        response: Response,
        user: UserSchema = Depends(validate_auth_user),
) -> TokenInfo:
    access = create_access_token(user)
    refresh = create_refresh_token(user)

    new_token_data = {
        "user_id": user.id,
        "token": refresh,
        "device_id": await get_device_id(request),
    }

    await TokenDAO.add(**new_token_data)

    update_for_user = {
        "active": True,
    }
    await UserDAO.update_by_id(instance_id=user.id, **update_for_user)

    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=False,
        samesite="strict",
        path="/auth/regenerate_access",
        max_age=60 * 60 * 24 * 7
    )

    return TokenInfo(
        access_token=access,
        refresh_token=refresh,
    )

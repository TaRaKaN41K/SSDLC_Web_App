from fastapi import Depends

from db.dao import UserDAO
from schemas import UserSchema, TokenInfo
from api.utils import create_access_token
from api.depends import get_current_auth_user_from_refresh


async def regenerate_access(
        user: UserSchema = Depends(get_current_auth_user_from_refresh),
) -> TokenInfo:
    access = create_access_token(user)

    update_for_user = {"active": True}
    await UserDAO.update_by_id(instance_id=user.id, **update_for_user)

    return TokenInfo(access_token=access)

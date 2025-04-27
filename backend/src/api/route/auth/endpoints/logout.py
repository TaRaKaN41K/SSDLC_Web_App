from fastapi import Depends, Response
from pydantic import BaseModel
from db.dao import TokenDAO, UserDAO
from schemas import UserSchema
from api.depends import get_current_active_auth_user


class ResponseModel(BaseModel):
    msg: str


async def logout(
        response: Response,
        user: UserSchema = Depends(get_current_active_auth_user),
) -> ResponseModel:
    await TokenDAO.delete_by_user_id(user_id=user.id)

    response.delete_cookie("refresh_token", path="/auth/regenerate_access")

    update_for_user = {"active": False}
    await UserDAO.update_by_id(instance_id=user.id, **update_for_user)

    return ResponseModel(msg="ok")

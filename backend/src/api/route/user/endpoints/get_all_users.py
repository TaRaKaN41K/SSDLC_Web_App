from pydantic import BaseModel
from typing import List
from db.dao import UserDAO


class Response(BaseModel):
    username: str
    email: str
    photo_filename: str


class PaginatedResponse(BaseModel):
    users: List[Response]
    total_pages: int
    current_page: int
    total_users: int


async def get_all_users(page: int, limit: int) -> PaginatedResponse:

    all_users = await UserDAO.get_all(page=page, limit=limit)
    total_users = await UserDAO.count_all()

    total_pages = (total_users // limit) + (1 if total_users % limit > 0 else 0)

    users_response: List[Response] = [
        Response(
            username=user["name"],
            email=user["email"],
            photo_filename=user["photo_filename"],
        )
        for user in all_users
    ]

    return PaginatedResponse(
        users=users_response,
        total_pages=total_pages,
        current_page=page,
        total_users=total_users
    )


from fastapi import Request

from api.utils import jwt_decode
from exceptions.custom_exceptions import AccessTokenNotFound, RefreshTokenNotFound


def get_token_from_request(request: Request, token_type: str) -> str:
    if token_type == "access":
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AccessTokenNotFound()

        return auth_header.split(" ")[1]

    elif token_type == "refresh":
        cookie = request.cookies.get("refresh_token")
        if not cookie:
            raise RefreshTokenNotFound()

        return cookie

    else:
        raise ValueError(f"Unknown token type: {token_type}")


def get_current_token_payload(token_type: str):
    async def _get_payload(request: Request) -> dict:
        token = get_token_from_request(request, token_type)
        return jwt_decode(token)
    return _get_payload

from datetime import timedelta

from . import create_jwt
from schemas import UserSchema
from config import settings
from logger import loggers


def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.name,
        "username": user.name,
        "email": user.email,
    }

    access_token = create_jwt(
        token_type="access",
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )

    loggers['auth'].info(f"Создан access токен для пользователя {user.name}")
    return access_token


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.name,
    }

    refresh_token = create_jwt(
        token_type="refresh",
        token_data=jwt_payload,
        expire_timedelta=timedelta(
            days=settings.auth_jwt.refresh_token_expire_days
        ),
    )

    loggers['auth'].info(f"Создан refresh токен для пользователя {user.name}")
    return refresh_token

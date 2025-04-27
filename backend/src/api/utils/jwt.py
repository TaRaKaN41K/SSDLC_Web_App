import jwt
from typing import Dict
from datetime import datetime, timedelta

from logger import loggers
from config import settings
from exceptions.custom_exceptions import (
    TokenExpiredError,
    InvalidTokenError,
    JWTEncodingError
)


def jwt_encode(
        payload: Dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()

    try:
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode.update(
            exp=expire,
            iat=now,
        )

        encoded = jwt.encode(
            payload=to_encode,
            key=private_key,
            algorithm=algorithm,
        )

        loggers['auth'].info(f"JWT токен успешно закодирован")
        return encoded

    except Exception as e:
        raise JWTEncodingError(f"Ошибка при кодировании JWT токена: {str(e)}")


def jwt_decode(
        token: str,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    try:
        decoded = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm]
        )

        loggers['auth'].info(f"JWT токен успешно декодирован")
        return decoded

    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("JWT token has expired")

    except jwt.InvalidTokenError as e:
        raise InvalidTokenError(f"Invalid JWT token: {str(e)}")


def create_jwt(
        token_type: str,
        token_data: Dict,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_data)
    token = jwt_encode(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )

    loggers['auth'].info(f"JWT токен успешно создан")
    return token

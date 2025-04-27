import bcrypt

from logger import loggers
from exceptions.custom_exceptions import InvalidPasswordError


def hash_password(
        password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)

    loggers['auth'].info(f"Пароль успешно захеширован.")
    return hashed_password


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    is_valid = bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )

    if is_valid:
        loggers['auth'].info("Пароль успешно проверен и совпадает.")
    else:
        raise InvalidPasswordError("Wrong password")

    return is_valid


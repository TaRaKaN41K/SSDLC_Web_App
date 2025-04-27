from typing import Optional
from fastapi import status

from exceptions.custom_exceptions.base import BaseAppException
from exceptions.error_code import *
from logger import loggers


class InvalidPasswordError(BaseAppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    message: str = "Wrong password"
    error_code: int = ErrorCode.INVALID_PASSWORD

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['auth'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)

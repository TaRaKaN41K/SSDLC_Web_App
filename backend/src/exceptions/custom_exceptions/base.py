from typing import Optional
from fastapi import status

from exceptions.error_code import *
from logger import loggers


class BaseAppException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Server error"
    error_code: int = ErrorCode.SERVER_ERROR

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['app'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)


class UnexpectedError(BaseAppException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "An unexpected mistake"
    error_code: int = ErrorCode.UNEXPECTED_ERROR

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['app'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)

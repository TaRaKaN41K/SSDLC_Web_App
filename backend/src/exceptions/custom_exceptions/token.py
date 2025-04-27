from typing import Optional
from fastapi import status

from exceptions.custom_exceptions.base import BaseAppException
from exceptions.error_code import *
from logger import loggers


class JWTEncodingError(BaseAppException):
    status_code: int = 500
    message: str = "Failed to encode JWT token"
    error_code: str = ErrorCode.SERVER_ERROR

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
        super().__init__(self.message)


class TokenExpiredError(BaseAppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    message: str = "JWT TOKEN is expired"
    error_code: int = ErrorCode.TOKEN_EXPIRED

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['auth'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)


class InvalidTokenError(BaseAppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    message: str = "Inappropriate JWT token"
    error_code: int = ErrorCode.INVALID_TOKEN

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['auth'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)


class InvalidTokenType(BaseAppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    message: str = "Invalid token type"
    error_code: int = ErrorCode.INVALID_TOKEN_TYPE

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['auth'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)


class AccessTokenNotFound(BaseAppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    message: str = "Access token missing"
    error_code: int = ErrorCode.INVALID_TOKEN_TYPE

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['auth'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)


class RefreshTokenNotFound(BaseAppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    message: str = "Refresh token missing"
    error_code: int = ErrorCode.INVALID_TOKEN_TYPE

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['auth'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)

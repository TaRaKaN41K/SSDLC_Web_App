from typing import Optional
from fastapi import status

from .base import BaseAppException
from exceptions.error_code import *
from logger import loggers


class ClienteIdentificationError(BaseAppException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = "Failed to identify client"
    error_code: int = ErrorCode.CLIENTE_IDENTIFICATION_ERROR

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['client'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)

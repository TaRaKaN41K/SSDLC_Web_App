from typing import Optional
from fastapi import status

from .base import BaseAppException
from exceptions.error_code import *
from logger import loggers


class ModelNotDefinedError(BaseAppException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "The model should be determined in the subclass"
    error_code: int = ErrorCode.MODEL_NOT_DEFINED

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['db'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)


class UniqueConstraintViolationError(BaseAppException):
    status_code: int = status.HTTP_409_CONFLICT
    message: str = "Violation of data uniqueness"
    error_code: int = ErrorCode.UNIQUE_CONSTRAINT_VIOLATION

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['db'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)


class RecordNotFoundError(BaseAppException):
    status_code: int = status.HTTP_404_NOT_FOUND
    message: str = "The record is not found"
    error_code: int = ErrorCode.RECORD_NOT_FOUND

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['db'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(message=self.message)


class FieldNotExistError(BaseAppException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = "The field does not exist in the model"
    error_code: int = ErrorCode.FIELD_NOT_EXIST

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['db'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)


class DatabaseError(BaseAppException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Database error"
    error_code: int = ErrorCode.DATABASE_ERROR

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['db'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)

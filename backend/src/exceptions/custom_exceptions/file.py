from typing import Optional
from fastapi import status

from exceptions.custom_exceptions.base import BaseAppException
from exceptions.error_code import *
from logger import loggers


class InvalidFileExtensionError(BaseAppException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = "An unacceptable file format"
    error_code: int = ErrorCode.INVALID_FILE_EXTENSION

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['utils'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)


class FileUploadError(BaseAppException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "File loading error"
    error_code: int = ErrorCode.FILE_UPLOAD_ERROR

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['utils'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)


class FileDeletionError(BaseAppException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "File deletion error"
    error_code: int = ErrorCode.FILE_DELETION_ERROR

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
            loggers['utils'].error(f"{self.__class__.__name__}: {self.message}")
        super().__init__(self.message)

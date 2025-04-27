from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from exceptions.error_code import ErrorCode
from exceptions.custom_exceptions import BaseAppException


async def app_http_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, BaseAppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.message,
                "error_code": exc.error_code,
            },
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Unexpected error occurred",
            "error_code": ErrorCode.SERVER_ERROR,
        },
    )

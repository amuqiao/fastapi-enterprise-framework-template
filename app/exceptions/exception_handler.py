from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from sqlalchemy.exc import IntegrityError
from app.exceptions.custom_exceptions import AppException


def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    if isinstance(exc, AppException):
        # 自定义异常处理
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_type,
                "detail": exc.detail,
                "path": request.url.path
            }
        )
    elif isinstance(exc, HTTPException):
        # FastAPI内置HTTP异常处理
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTPError",
                "detail": exc.detail,
                "path": request.url.path
            }
        )
    elif isinstance(exc, RequestValidationError):
        # 请求验证异常处理
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "ValidationError",
                "detail": exc.errors(),
                "path": request.url.path
            }
        )
    elif isinstance(exc, IntegrityError):
        # 数据库完整性异常处理
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "IntegrityError",
                "detail": "Database integrity constraint violation",
                "path": request.url.path
            }
        )
    else:
        # 其他未处理异常
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "detail": "An unexpected error occurred",
                "path": request.url.path
            }
        )

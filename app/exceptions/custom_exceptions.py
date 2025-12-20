class AppException(Exception):
    """应用基础异常类"""
    def __init__(self, status_code: int, detail: str, error_type: str = "AppError"):
        self.status_code = status_code
        self.detail = detail
        self.error_type = error_type
        super().__init__(self.detail)


class AuthenticationError(AppException):
    """认证错误异常"""
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail, error_type="AuthenticationError")


class AuthorizationError(AppException):
    """授权错误异常"""
    def __init__(self, detail: str):
        super().__init__(status_code=403, detail=detail, error_type="AuthorizationError")


class ValidationError(AppException):
    """验证错误异常"""
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail, error_type="ValidationError")


class NotFoundError(AppException):
    """资源不存在异常"""
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail=detail, error_type="NotFoundError")


class ConflictError(AppException):
    """资源冲突异常"""
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail, error_type="ConflictError")

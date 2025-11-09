from .base_exception import AppException

class UserAlreadyExists(AppException):
    pass

class UserNotFound(AppException):
    pass
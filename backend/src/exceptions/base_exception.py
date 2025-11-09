class AppException(Exception):
    """Base class for all application exceptions."""
    pass

class ForbiddenOperationException(AppException):
    """Exception raised for forbidden operations."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

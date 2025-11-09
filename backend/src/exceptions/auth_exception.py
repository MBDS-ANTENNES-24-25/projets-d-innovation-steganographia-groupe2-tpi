from src.exceptions.base_exception import AppException

class NotAuthenticatedException(AppException):
    def __init__(self):
        self.message = "Not authenticated"
        super().__init__(self.message)

class InvalidCredentialsException(AppException):
    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = "Invalid email or password"
        super().__init__(self.message)


class InactiveUserException(AppException):
    def __init__(self):
        self.message = "User account is inactive"
        super().__init__(self.message)

class OAuthTokenException(AppException):
    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = "OAuth token is invalid or expired"
        super().__init__(self.message)

class OAuthOnlyUserException(AppException):
    def __init__(self):
        self.message = "This user can only log in via OAuth"
        super().__init__(self.message)

class RefreshTokenInvalidException(AppException):
    def __init__(self):
        self.message = "Refresh token is invalid"
        super().__init__(self.message)
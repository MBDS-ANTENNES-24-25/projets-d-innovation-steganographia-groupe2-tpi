from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.exceptions.base_exception import ForbiddenOperationException
from src.exceptions.auth_exception import InactiveUserException, InvalidCredentialsException, NotAuthenticatedException, OAuthOnlyUserException, OAuthTokenException, RefreshTokenInvalidException

from .user_exception import UserAlreadyExists, UserNotFound
from .role_exception import RoleNotFound
from .status_exception import StatusNotFound

def add_exception_handlers(app):
    """ General exception handler """
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(status_code=400, content={"err": str(exc)})

    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(request: Request, exc: RequestValidationError):
        first_error = exc.errors()[0]
        return JSONResponse(status_code=422, content={"err": first_error["msg"]})
    
    
    """ Forbidden operation """
    @app.exception_handler(ForbiddenOperationException)
    async def forbidden_operation_handler(request: Request, exc: Exception):
        if hasattr(exc, 'message'):
            return JSONResponse(status_code=403, content={"err": exc.message})
        return JSONResponse(status_code=403, content={"err": "You are not allowed to perform this operation."})


    """ User and everything connected with it """ 
    @app.exception_handler(UserAlreadyExists)
    async def user_already_exists_handler(request: Request, exc: UserAlreadyExists):
        return JSONResponse(status_code=400, content={"err": str(exc)})

    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(request: Request, exc: UserNotFound):
        return JSONResponse(status_code=404, content={"err": str(exc)})

    @app.exception_handler(RoleNotFound)
    async def role_not_found_handler(request: Request, exc: RoleNotFound):
        return JSONResponse(status_code=404, content={"err": str(exc)})

    @app.exception_handler(StatusNotFound)
    async def status_not_found_handler(request: Request, exc: StatusNotFound):
        return JSONResponse(status_code=404, content={"err": str(exc)})
    

    """ Login """
    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
        return JSONResponse(status_code=401, content={"err": exc.message})

    @app.exception_handler(InactiveUserException)
    async def inactive_user_handler(request: Request, exc: InactiveUserException):
        return JSONResponse(status_code=403, content={"err": exc.message})
    
    @app.exception_handler(NotAuthenticatedException)
    async def not_authenticated_handler(request: Request, exc: NotAuthenticatedException):
        return JSONResponse(status_code=401, content={"err": exc.message})
    

    """ OAuth """
    @app.exception_handler(OAuthTokenException)
    async def oauth_token_exception_handler(request: Request, exc: OAuthTokenException):
        return JSONResponse(status_code=401, content={"err": exc.message})

    @app.exception_handler(OAuthOnlyUserException)
    async def oauth_only_user_handler(request: Request, exc: OAuthOnlyUserException):
        return JSONResponse(status_code=403, content={"err": exc.message})


    """ Refresh token """
    @app.exception_handler(RefreshTokenInvalidException)
    async def refresh_token_invalid_handler(request: Request, exc: RefreshTokenInvalidException):
        return JSONResponse(status_code=401, content={"err": exc.message})
    

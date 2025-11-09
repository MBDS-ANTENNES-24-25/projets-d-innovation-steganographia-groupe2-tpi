from fastapi import APIRouter, Depends, Request, Response, BackgroundTasks
from fastapi.responses import RedirectResponse
from src.schemas.auth_schema import LoginRequest, ResetPasswordRequest, TokenResponse, ForgotPasswordRequest
from src.schemas.user_schema import UserCreate, UserRead
from src.services.auth_service import AuthService
from src.services.google_auth_service import GoogleAuthService
from src.dependencies.injection import get_auth_service, get_current_user, get_google_auth_service
from src.utils.cookies import set_refresh_token_cookie
from src.schemas.base_schema import BaseErrorResponse, BaseMessageResponse


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register",
    status_code=201,
    responses={
        201: {"model": UserRead, "description": "User created successfully."},
        422: {"model": BaseErrorResponse, "description": "Validation Error"}
    }
)
def register_user(
    data: UserCreate,
    background_tasks: BackgroundTasks, 
    auth_service: AuthService = Depends(get_auth_service)
):
    user = auth_service.register_user(
        firstname=data.firstname,
        lastname=data.lastname,
        username=data.username,
        email=data.email,
        password=data.password,
        background_tasks=background_tasks
    )
    return user
    

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=200,
    responses={
        200: {"model": TokenResponse, "description": "Login successful."},
        401: {"model": BaseErrorResponse, "description": "Invalid credentials."},
        422: {"model": BaseErrorResponse, "description": "Validation Error"}
    }
)
def login(
    data: LoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
):
    access_token, refresh_token, _ = auth_service.login(data.email, data.password)
    set_refresh_token_cookie(response, refresh_token)

    return {"access_token": access_token}


@router.get(
    "/google/login",
    status_code=200,
    responses={
        200: {"description": "Google OAuth login URL."}
    }
)
async def login_with_google(
    google_auth_service: GoogleAuthService = Depends(get_google_auth_service)
):
    auth_url = google_auth_service.get_google_auth_url()
    return {"auth_url": auth_url}


@router.get(
    "/google/callback",
    response_model=TokenResponse,
    status_code=200,
    responses={
        200: {"model": TokenResponse, "description": "Google login successful."},
        400: {"model": BaseErrorResponse, "description": "Invalid Google authentication code."},
        422: {"model": BaseErrorResponse, "description": "Validation Error"}
    }
)
async def google_callback(
    code: str,
    response: Response,
    google_auth_service: GoogleAuthService = Depends(get_google_auth_service)
):
    access_token, refresh_token, _ = google_auth_service.authenticate_with_google(code)
    set_refresh_token_cookie(response, refresh_token)

    return {"access_token": access_token}


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=200,
    responses={
        200: {"model": TokenResponse, "description": "Token refreshed successfully."},
        401: {"model": BaseErrorResponse, "description": "Invalid or expired refresh token."},
        422: {"model": BaseErrorResponse, "description": "Validation Error"}
    }
)
def refresh_token(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
    refresh_token = request.cookies.get("refresh_token")
    new_access_token = auth_service.refresh_access_token(refresh_token)
    return {"access_token": new_access_token, "token_type": "bearer"}
    

@router.post(
    "/logout",
    status_code=200,
    responses={
        200: {"description": "Logged out successfully."}
    }
)
def logout_user(response: Response):
    response.delete_cookie("refresh_token")
    return {"msg": "Logged out successfully"}

@router.get(
    "/me",
    response_model=UserRead,
    status_code=200,
    responses={
        200: {"model": UserRead, "description": "Current user information."},
        401: {"model": BaseErrorResponse, "description": "Not authenticated."}
    }
)
def get_me(current_user: UserRead = Depends(get_current_user)):
    return current_user


@router.post(
    "/forgot-password",
    status_code=200,
    responses={
        200: {"model": BaseMessageResponse, "description": "If the email exists, a reset link has been sent."},
        422: {"model": BaseErrorResponse, "description": "Validation Error"}
    }
)
def forgot_password(
    request: ForgotPasswordRequest, 
    background_tasks: BackgroundTasks, 
    auth_service: AuthService = Depends(get_auth_service),
    req: Request = None
):
    client_ip = req.client.host if req and req.client else None
    auth_service.forgot_password(request.email, client_ip, background_tasks)
    return {"msg": "If the email exists, a reset link has been sent."}


@router.post(
    "/reset-password",
    status_code=200,
    responses={
        200: {"model": BaseMessageResponse, "description": "Password has been reset successfully."},
        400: {"model": BaseErrorResponse, "description": "Invalid or expired reset token."},
        422: {"model": BaseErrorResponse, "description": "Validation Error"}
    }
)
def reset_password(
    request: ResetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.reset_password(request.token, request.new_password)
    return {"msg": "Password has been reset successfully."}


@router.post(
    "/confirm-email",
    status_code=200,
    responses={
        200: {"model": BaseMessageResponse, "description": "Email confirmed successfully."},
        400: {"model": BaseErrorResponse, "description": "Invalid or expired confirmation token."},
        422: {"model": BaseErrorResponse, "description": "Validation Error"}
    }
)
def confirm_email(
    token: str, 
    auth_service: AuthService = Depends(get_auth_service)
):
    user = auth_service.confirm_email(token)
    return {"msg": "Email confirmed successfully.", "user": user}


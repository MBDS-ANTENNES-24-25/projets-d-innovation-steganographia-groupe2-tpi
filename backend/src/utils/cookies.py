from fastapi import Response
from src.core.config import settings

def set_refresh_token_cookie(response: Response, refresh_token: str):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=(settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600)
    )

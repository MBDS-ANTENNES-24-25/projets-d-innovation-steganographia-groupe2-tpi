import httpx
from src.core.config import settings

def exchange_google_code(code: str) -> dict | None:
    resp = httpx.post("https://oauth2.googleapis.com/token", data={
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    })
    return resp.json() if resp.status_code == 200 else None


def get_google_user_info(access_token: str) -> dict | None:
    resp = httpx.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return resp.json() if resp.status_code == 200 else None

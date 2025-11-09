from sqlalchemy.orm import Session
from src.schemas.role_schema import RoleEnum
from src.schemas.status_schema import StatusEnum
from src.services.role_service import RoleService
from src.services.status_service import StatusService
from src.services.user_role_service import UserRoleService
from src.services.user_status_service import UserStatusService
from src.services.user_service import UserService
from src.utils.security import generate_tokens_for_user
from src.utils.google_oauth import exchange_google_code, get_google_user_info
from src.models.user import User
from src.exceptions.auth_exception import OAuthTokenException
from urllib.parse import urlencode
from src.core.config import settings

class GoogleAuthService:
    def __init__(
        self, 
        db: Session,
        user_service: UserService,
        role_service: RoleService,
        status_service: StatusService,
        user_role_service: UserRoleService,
        user_status_service: UserStatusService,
    ):
        self.db = db
        self.user_service = user_service
        self.role_service = role_service
        self.status_service = status_service
        self.user_role_service = user_role_service
        self.user_status_service = user_status_service

    def get_google_auth_url(self) -> str:
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        query = urlencode({
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent"
        })
        return f"{base_url}?{query}"


    def authenticate_with_google(self, code: str) -> tuple[str, str, User]:
        token_data = exchange_google_code(code)
        if not token_data:
            raise OAuthTokenException("Google token exchange failed")

        user_info = get_google_user_info(token_data["access_token"])
        if not user_info or "email" not in user_info:
            raise OAuthTokenException("Invalid user info")

        user = self.user_service.get_by_email(user_info["email"])
        if not user:
            try:
                user = self.user_service.create_user_oauth(
                    email=user_info["email"],
                    firstname=user_info.get("given_name", ""),
                    lastname=user_info.get("family_name", ""),
                    provider="google",
                    commit=False
                )

                role = self.role_service.get_by_name(RoleEnum.END_USER)
                self.user_role_service.assign_role(user.id, role.id, commit=False)

                status = self.status_service.get_by_name(StatusEnum.ACTIVE) 
                self.user_status_service.assign_status(user.id, status.id, reason="Initial registration", commit=False)

                self.db.commit()
                self.db.refresh(user)
            except Exception as e:
                self.db.rollback()
                raise e

        access_token, refresh_token = generate_tokens_for_user(user.id)

        return access_token, refresh_token, user

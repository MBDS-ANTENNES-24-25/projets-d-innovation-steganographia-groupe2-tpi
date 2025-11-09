from datetime import datetime, timedelta
import secrets
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.core.config import settings
from src.services.password_history_service import PasswordHistoryService
from src.services.password_reset_token_service import PasswordResetTokenService
from src.exceptions.auth_exception import InactiveUserException, InvalidCredentialsException, NotAuthenticatedException, OAuthOnlyUserException, RefreshTokenInvalidException
from src.schemas.auth_schema import TokenPayload, EmailConfirmationPayload

from src.schemas.role_schema import RoleEnum
from src.schemas.status_schema import StatusEnum
from src.services.role_service import RoleService
from src.services.status_service import StatusService
from src.services.user_role_service import UserRoleService
from src.services.user_service import UserService
from src.services.user_status_service import UserStatusService
from src.utils.security import create_access_token, create_email_confirmation_token, decode_jwt, generate_tokens_for_user, get_password_hash, verify_password
from src.utils.mail import send_mail


class AuthService:
    def __init__(
        self,
        db: Session,
        user_service: UserService,
        role_service: RoleService,
        status_service: StatusService,
        user_role_service: UserRoleService,
        user_status_service: UserStatusService,
        password_history_service: PasswordHistoryService,
        password_reset_token_service: PasswordResetTokenService
    ):
        self.db = db
        self.user_service = user_service
        self.role_service = role_service
        self.status_service = status_service
        self.user_role_service = user_role_service
        self.user_status_service = user_status_service
        self.password_history_service = password_history_service
        self.password_reset_token_service = password_reset_token_service

    def register_user(self, firstname: str, lastname: str, username: str, email: str, password: str, background_tasks=None):
        try:
            hashed_password = get_password_hash(password)
            user = self.user_service.create_user(firstname, lastname, username, email, hashed_password, commit=False)

            if self.password_history_service.is_password_reused(user.id, hashed_password):
                raise InvalidCredentialsException("Password has been used before. Please choose a different password.")
            self.password_history_service.add_password_history(user.id, hashed_password, commit=False)

            role = self.role_service.get_by_name(RoleEnum.END_USER)
            self.user_role_service.assign_role(user.id, role.id, commit=False)

            status = self.status_service.get_by_name(StatusEnum.INACTIVE) 
            self.user_status_service.assign_status(user.id, status.id, reason="Initial registration", commit=False)

            email_confirmation_token = create_email_confirmation_token(user.email)
            if background_tasks:
                background_tasks.add_task(self.send_email_confirmation, user.email, email_confirmation_token)
            else:
                self.send_email_confirmation(user.email, email_confirmation_token)

            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise e
    

    def login(self, email: str, password: str):
        user = self.user_service.get_by_email(email)
        if not user:
            raise InvalidCredentialsException()

        # NOTE: Uncomment the following lines if you want to show an error for OAuth users
        # if user.is_oauth:
        #     oauth_provider = user.oauth_provider.title()
        #     raise OAuthOnlyUserException(f"This account is linked to {oauth_provider}. Please login with {oauth_provider}.")

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()
        
        status = self.user_status_service.get_current_status(user.id)
        if status is StatusEnum.INACTIVE:
            raise InactiveUserException()
        
        access_token, refresh_token = generate_tokens_for_user(user.id)

        return access_token, refresh_token, user
    

    def refresh_access_token(self, refresh_token: str) -> str:
        if refresh_token is None:
            raise NotAuthenticatedException()
        
        payload = decode_jwt(refresh_token)
        token_data = TokenPayload(**payload)

        user = self.user_service.get_by_id(token_data.sub)
        if not user or self.user_status_service.get_current_status(user.id) != StatusEnum.ACTIVE:
            raise RefreshTokenInvalidException()

        return create_access_token({"sub": str(user.id)})


    def send_reset_password_email(self, email: str, token: str):
        reset_link = f"{settings.FRONTEND_RESET_PASSWORD_URL}{token}"
        env = Environment(
            loader=FileSystemLoader("src/templates"),
            autoescape=select_autoescape(["html", "xml"])
        )
        template = env.get_template("reset_password_email.html")
        html_content = template.render(
            reset_link=reset_link,
            exp=settings.RESET_PASSWORD_EXPIRE_MINUTES
        )
        subject = "SteganographIA - Password Reset Request"
        send_mail([email], subject, html_content)


    def forgot_password(self, email: str, ip_address: str, background_tasks=None):
        user = self.user_service.get_by_email(email)
        if user:
            if not self.password_reset_token_service.can_request_reset(email=email, ip_address=ip_address, max_requests=settings.MAX_PASSWORD_RESET_REQUESTS):
                raise ValueError("Too many password reset requests. Please try again later.") # TODO: Custom exception can be used here

            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(minutes=settings.RESET_PASSWORD_EXPIRE_MINUTES)
            self.password_reset_token_service.create_reset_token(user.id, ip_address, token, expires_at)
            if background_tasks:
                background_tasks.add_task(self.send_reset_password_email, user.email, token)
            else:
                self.send_reset_password_email(user.email, token)


    def reset_password(self, token: str, new_password: str):
        try:
            token_obj = self.password_reset_token_service.mark_token_as_used(token, commit=False)
            user = self.user_service.get_by_id(token_obj.user_id, raise_exc=True)

            user = self.user_service.get_by_email(user.email, raise_exc=True)
            hashed_password = get_password_hash(new_password)
            
            if self.password_history_service.is_password_reused(user.id, new_password):
                raise InvalidCredentialsException("Password has been used before. Please choose a different password.")

            user.password = hashed_password
            self.password_history_service.add_password_history(user.id, hashed_password, commit=False)

            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise e


    def send_email_confirmation(self, email: str, token: str):
        confirmation_link = f"{settings.FRONTEND_CONFIRM_EMAIL_URL}{token}"
        env = Environment(
            loader=FileSystemLoader("src/templates"),
            autoescape=select_autoescape(["html", "xml"])
        )
        template = env.get_template("confirm_email.html")
        html_content = template.render(
            confirmation_link=confirmation_link, 
            exp=settings.EMAIL_CONFIRMATION_EXPIRE_MINUTES
        )
        subject = "SteganographIA - Email Confirmation"
        send_mail([email], subject, html_content)


    def confirm_email(self, token: str):
        try:
            payload = decode_jwt(token)
            token_data = TokenPayload(**payload)
            email = token_data.email
            user = self.user_service.get_by_email(email, raise_exc=True)

            user_status = self.user_status_service.get_current_status(user.id)
            if user_status != StatusEnum.INACTIVE:
                raise InvalidCredentialsException("Email is already confirmed or user is active.")

            active_status = self.status_service.get_by_name(StatusEnum.ACTIVE)
            self.user_status_service.assign_status(user.id, active_status.id, reason="Email confirmed", commit=False)

            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise e


    def validate_token_and_get_user(self, token: str):
        if not token:
            raise NotAuthenticatedException()
        
        token_payload = decode_jwt(token)
        token_data = TokenPayload(**token_payload)

        user = self.user_service.get_by_id(token_data.sub)
        if not user:
            raise InvalidCredentialsException()

        user_status = self.user_status_service.get_current_status(user.id)
        if user_status != StatusEnum.ACTIVE:
            raise InactiveUserException()
        
        return user
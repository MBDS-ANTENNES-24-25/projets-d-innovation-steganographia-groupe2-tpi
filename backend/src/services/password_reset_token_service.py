from sqlalchemy.orm import Session

from src.models.password_reset_token import PasswordResetToken
from src.repositories.password_reset_token_repository import PasswordResetTokenRepository
from datetime import datetime, timedelta

class PasswordResetTokenService:
    def __init__(
        self, 
        db: Session, 
        password_reset_token_repository: PasswordResetTokenRepository
    ):
        self.db = db
        self.password_reset_token_repository = password_reset_token_repository

    def create_reset_token(self, user_id: int, ip_address: str, token: str, expires_at: str) -> PasswordResetToken:
        return self.password_reset_token_repository.create(user_id, ip_address, token, expires_at)


    def get_valid_token(self, token: str, raise_exc: bool = False) -> PasswordResetToken:
        token_obj = self.password_reset_token_repository.get_valid_token(token)
        if not token_obj and raise_exc:
            raise ValueError("Invalid or expired token") # TODO: Custom exception can be used here
        return token_obj


    def mark_token_as_used(self, token: str, commit: bool = True) -> PasswordResetToken:
        token_obj = self.get_valid_token(token, raise_exc=True)
        self.password_reset_token_repository.mark_as_used(token_obj, commit)
        self.password_reset_token_repository.update_date_of_use(token_obj, commit)
        return token_obj 
    

    def can_request_reset(self, email: str = None, ip_address: str = None, window_minutes: int = 15, max_requests: int = 1) -> bool:
        window_start = datetime.now() - timedelta(minutes=window_minutes)
        count = 0

        if email:
            count += self.password_reset_token_repository.count_requests_by_email_since(email=email, since=window_start)
        if ip_address:
            count += self.password_reset_token_repository.count_requests_by_ip_since(ip_address=ip_address, since=window_start)

        return count < max_requests

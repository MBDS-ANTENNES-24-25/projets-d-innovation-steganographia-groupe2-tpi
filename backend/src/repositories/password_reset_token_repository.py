from datetime import datetime
from sqlalchemy.orm import Session
from src.models import User
from src.models.password_reset_token import PasswordResetToken

class PasswordResetTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, ip_address: str, token: str, expires_at: datetime):
        reset = PasswordResetToken(user_id=user_id,  ip_address=ip_address, token=token, expires_at=expires_at)
        self.db.add(reset)
        self.db.commit()
        return reset


    def get_valid_token(self, token: str):
        return self.db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.used == False,
            PasswordResetToken.expires_at > datetime.now()
        ).first()
    
    
    def get_latest_by_email(self, user_id: int):
        return self.db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user_id
        ).order_by(PasswordResetToken.created_at.desc()).first()


    def get_latest_by_ip(self, ip_address: str):
        return self.db.query(PasswordResetToken).filter(
            PasswordResetToken.ip_address == ip_address
        ).order_by(PasswordResetToken.created_at.desc()).first()


    def mark_as_used(self, token_obj: PasswordResetToken, commit: bool = True):
        token_obj.used = True
        if commit:
            self.db.commit()

    
    def update_date_of_use(self, token_obj: PasswordResetToken, commit: bool = True):
        token_obj.date_of_use = datetime.now()
        if commit:
            self.db.commit()


    def count_requests_by_email_since(self, email: str, since: datetime = None):
        query = self.db.query(PasswordResetToken).join(User).filter_by(email=email)
        if since is not None:
            query = query.filter(PasswordResetToken.created_at >= since)
        return query.count()


    def count_requests_by_ip_since(self, ip_address: str, since: datetime = None):
        query = self.db.query(PasswordResetToken).filter(PasswordResetToken.ip_address == ip_address)
        if since is not None:
            query = query.filter(PasswordResetToken.created_at >= since)
        return query.count()

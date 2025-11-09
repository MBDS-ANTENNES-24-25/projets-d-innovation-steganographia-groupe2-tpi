from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from src.db.base import Base

class PasswordResetToken(Base):
    __tablename__ = "password_reset_token"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    ip_address = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    date_of_use = Column(DateTime, nullable=True)

    user = relationship("User")
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship
from src.db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_oauth = Column(Boolean, default=False)
    oauth_provider = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    status_history = relationship("UserStatus", back_populates="user")
    roles = relationship("UserRole", back_populates="user")
    password_history = relationship("PasswordHistory", back_populates="user", cascade="all, delete-orphan")

    verifications = relationship("Verification", back_populates="verifier")
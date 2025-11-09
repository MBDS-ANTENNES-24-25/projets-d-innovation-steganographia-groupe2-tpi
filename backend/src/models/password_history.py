from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from src.db.base import Base

class PasswordHistory(Base):
    __tablename__ = "password_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    password = Column(String, nullable=False)  # hashed
    changed_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="password_history")

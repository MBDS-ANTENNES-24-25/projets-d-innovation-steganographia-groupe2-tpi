from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from src.db.base import Base


class UserStatus(Base):
    __tablename__ = "user_status"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String(255), nullable=True)

    user = relationship("User", back_populates="status_history")
    status = relationship("Status", back_populates="user_statuses")

from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship
from src.db.base import Base


class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")

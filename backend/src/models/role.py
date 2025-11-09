from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.base import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g., 'admin', 'end_user'
    description = Column(String(255), nullable=True)

    users = relationship("UserRole", back_populates="role")

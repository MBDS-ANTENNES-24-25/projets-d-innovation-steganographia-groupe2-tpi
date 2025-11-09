from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.base import Base


class Status(Base):
    """
    Represents the status of a user account in the system.
    Attributes:
        id (int): Primary key identifier for the status.
        name (str): Unique name of the status (e.g., 'active', 'inactive', 'suspended').
        description (str, optional): Additional details about the status.
        user_statuses (List[UserStatus]): Relationship to the UserStatus history records.
    Notes:
        - By default, a newly created account is set to 'inactive'.
        - The account becomes 'active' when the user activates it using the provided URL.
        - The account can be set to 'suspended' by an admin action.
        - The account is by default 'active' if the user is authenticated via Google.
    """
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    user_statuses = relationship("UserStatus", back_populates="status")

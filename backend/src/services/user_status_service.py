from sqlalchemy.orm import Session
from src.schemas.status_schema import StatusEnum
from src.models.user_status import UserStatus
from src.repositories.user_status_repository import UserStatusRepository

class UserStatusService:
    def __init__(self, db: Session, user_status_repository: UserStatusRepository):
        self.db = db
        self.user_status_repository = user_status_repository

    def assign_status(self, user_id: int, status_id: int, reason: str = None, commit: bool = True) -> UserStatus:
        return self.user_status_repository.create(
            user_id=user_id,
            status_id=status_id,
            reason=reason,
            commit=commit
        )


    def get_current_status(self, user_id: int) -> StatusEnum:
        return self.user_status_repository.get_latest_status(user_id)
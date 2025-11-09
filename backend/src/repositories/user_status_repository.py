from sqlalchemy.orm import Session
from src.models.status import Status
from src.schemas.status_schema import StatusEnum
from src.models.user_status import UserStatus
from datetime import datetime

class UserStatusRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, status_id: int, reason: str = None, commit: bool = True):
        self.db.add(UserStatus(
            user_id=user_id,
            status_id=status_id,
            reason=reason
        ))
        if commit:
            self.db.commit()


    def get_latest_status(self, user_id: int) -> StatusEnum:
        status = (
            self.db.query(Status.name)
            .join(UserStatus, Status.id == UserStatus.status_id)
            .filter(UserStatus.user_id == user_id)
            .order_by(UserStatus.changed_at.desc())
            .first()
        )
        return StatusEnum(status[0]) if status else None
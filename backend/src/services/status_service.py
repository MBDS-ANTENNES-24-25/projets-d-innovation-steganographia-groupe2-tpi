from sqlalchemy.orm import Session
from src.repositories.status_repository import StatusRepository
from src.models.status import Status
from src.exceptions.status_exception import StatusNotFound

class StatusService:
    def __init__(self, db: Session, status_repo: StatusRepository):
        self.db = db
        self.status_repo = status_repo

    def get_by_name(self, name: str) -> Status:
        status = self.status_repo.get_by_name(name)
        if not status:
            raise StatusNotFound(f"Status '{name}' not found")
        return status

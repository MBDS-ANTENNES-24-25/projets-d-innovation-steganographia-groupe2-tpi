from typing import Optional
from sqlalchemy.orm import Session

from src.models import Status 

class StatusRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Optional[Status]:
        return self.db.query(Status).filter(Status.name == name).first()
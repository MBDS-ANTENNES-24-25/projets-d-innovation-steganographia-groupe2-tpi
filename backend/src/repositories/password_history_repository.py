from sqlalchemy.orm import Session
from src.models.password_history import PasswordHistory

class PasswordHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, hashed_password: str, commit: bool = True):
        entry = PasswordHistory(user_id=user_id, password=hashed_password)
        self.db.add(entry)
        self.db.flush()
        if commit:
            self.db.commit()
            self.db.refresh(entry)
        return entry
    
    
    def get_list_by_user(self, user_id: int):
        return (
            self.db.query(PasswordHistory)
            .filter_by(user_id=user_id)
            .order_by(PasswordHistory.changed_at.desc())
            .all()
        )

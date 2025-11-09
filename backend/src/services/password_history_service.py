
from sqlalchemy.orm import Session

from src.repositories.password_history_repository import PasswordHistoryRepository
from src.utils.security import verify_password


class PasswordHistoryService:
    def __init__(
        self, 
        db: Session, 
        password_history_repository: PasswordHistoryRepository
    ):
        self.db = db
        self.password_history_repository = password_history_repository

    def add_password_history(self, user_id: int, hashed_password: str, commit: bool = True) -> PasswordHistoryRepository:
        return self.password_history_repository.create(user_id, hashed_password, commit)


    def is_password_reused(self, user_id: int, plain_password: str) -> bool:
        password_histories = self.password_history_repository.get_list_by_user(user_id)
        for history in password_histories:
            if verify_password(plain_password, history.password):
                return True
        return False

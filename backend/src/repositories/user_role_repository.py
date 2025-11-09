from sqlalchemy.orm import Session
from src.models.role import Role
from src.models.user_role import UserRole

class UserRoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, role_id: int, commit: bool = True):
        self.db.add(UserRole(user_id=user_id, role_id=role_id))
        if commit:
            self.db.commit()


    def has_user_role(self, user_id: int, role_name: str) -> bool:
        return (
            self.db.query(UserRole)
            .join(Role, Role.id == UserRole.role_id)
            .filter(UserRole.user_id == user_id, Role.name == role_name)
            .first()
            is not None
        )
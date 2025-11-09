from sqlalchemy.orm import Session
from src.schemas.role_schema import RoleEnum
from src.repositories.user_role_repository import UserRoleRepository
from src.models.user_role import UserRole

class UserRoleService:
    def __init__(
        self, 
        db: Session, 
        user_role_repository: UserRoleRepository
    ):
        self.db = db
        self.user_role_repository = user_role_repository

    def assign_role(self, user_id: int, role_id: int, commit: bool = True) -> UserRole:
        return self.user_role_repository.create(user_id, role_id, commit)
    

    def has_role(self, user_id: int, role: RoleEnum) -> bool:
        return self.user_role_repository.has_user_role(user_id, role)

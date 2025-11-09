from sqlalchemy.orm import Session
from src.repositories.role_repository import RoleRepository
from src.models.role import Role
from src.exceptions.role_exception import RoleNotFound

class RoleService:
    def __init__(self, db: Session, role_repo: RoleRepository):
        self.db = db
        self.role_repo = role_repo

    def get_by_name(self, name: str) -> Role:
        role = self.role_repo.get_by_name(name)
        if not role:
            raise RoleNotFound(f"Role '{name}' not found")
        return role

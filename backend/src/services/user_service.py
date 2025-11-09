from sqlalchemy.orm import Session
from src.services.status_service import StatusService
from src.exceptions.base_exception import ForbiddenOperationException
from src.schemas.role_schema import RoleEnum
from src.schemas.status_schema import StatusEnum
from src.services.user_role_service import UserRoleService
from src.services.user_status_service import UserStatusService
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.exceptions.user_exception import UserAlreadyExists, UserNotFound

class UserService:
    def __init__(
        self, 
        db: Session, 
        user_repository: UserRepository,
        status_service: StatusService,
        user_role_service: UserRoleService,
        user_status_service: UserStatusService
    ):
        self.db = db
        self.user_repository = user_repository
        self.status_service = status_service
        self.user_role_service = user_role_service
        self.user_status_service = user_status_service

    def create_user(self, firstname: str, lastname: str, username: str, email: str, hashed_password: str, commit: bool = True) -> User:
        if self.user_repository.get_by_email(email):
            raise UserAlreadyExists(f"Email '{email}' already registered")
        if self.user_repository.get_by_username(username):
            raise UserAlreadyExists(f"Username '{username}' already taken")

        return self.user_repository.create(firstname, lastname, username, email, hashed_password, commit=commit)
    
    
    def create_user_oauth(self, email: str, firstname: str, lastname: str, provider: str, commit: bool = True) -> User:
        username = email.split('@')[0]
        return self.user_repository.create_user_oauth(email, firstname, lastname, username, provider, commit=commit)


    def get_by_email(self, email: str, raise_exc: bool = False):
        user = self.user_repository.get_by_email(email)
        if not user and raise_exc:
            raise UserNotFound(f"User with email '{email}' not found.")
        return user


    def get_by_username(self, username: str, raise_exc: bool = False):
        user = self.user_repository.get_by_username(username)
        if not user and raise_exc:
            raise UserNotFound(f"User with username '{username}' not found.")
        return user


    def get_by_id(self, user_id: int, raise_exc: bool = False):
        user = self.user_repository.get_by_id(user_id)
        if not user and raise_exc:
            raise UserNotFound(f"User with ID '{user_id}' not found.")
        return user

    
    def deactivate_end_user(self, user_id: int):
        user = self.get_by_id(user_id, raise_exc=True)
        if not self.user_role_service.has_role(user.id, RoleEnum.END_USER):
            raise ForbiddenOperationException("Only end users can be deactivated.")

        inactive_status = self.status_service.get_by_name(StatusEnum.INACTIVE)
        self.user_status_service.assign_status(
            user_id=user_id,
            status_id=inactive_status.id,
            reason="Account deactivated by admin"
        )

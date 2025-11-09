from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session

from src.services.google_auth_service import GoogleAuthService
from src.services.password_reset_token_service import PasswordResetTokenService
from src.repositories.password_history_repository import PasswordHistoryRepository
from src.repositories.password_reset_token_repository import PasswordResetTokenRepository
from src.services.password_history_service import PasswordHistoryService
from src.models.user import User
from src.exceptions.auth_exception import InvalidCredentialsException
from src.db.deps import get_db

from src.repositories.user_repository import UserRepository
from src.repositories.role_repository import RoleRepository
from src.repositories.status_repository import StatusRepository
from src.repositories.user_status_repository import UserStatusRepository
from src.repositories.user_role_repository import UserRoleRepository

from src.services.user_service import UserService
from src.services.role_service import RoleService
from src.services.status_service import StatusService
from src.services.user_status_service import UserStatusService
from src.services.user_role_service import UserRoleService
from src.services.auth_service import AuthService
from src.services.stego_service import StegoService
from fastapi import Request


# Repositories injections
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_role_repository(db: Session = Depends(get_db)) -> RoleRepository:
    return RoleRepository(db)

def get_status_repository(db: Session = Depends(get_db)) -> StatusRepository:
    return StatusRepository(db)

def get_user_status_repository(db: Session = Depends(get_db)) -> UserStatusRepository:
    return UserStatusRepository(db)

def get_user_role_repository(db: Session = Depends(get_db)) -> UserRoleRepository:
    return UserRoleRepository(db)

def get_password_history_repository(db: Session = Depends(get_db)) -> PasswordHistoryRepository:
    return PasswordHistoryRepository(db)

def get_password_reset_token_repository(db: Session = Depends(get_db)) -> PasswordResetTokenRepository:
    return PasswordResetTokenRepository(db)

def get_stego_service(db: Session = Depends(get_db)) -> StegoService:
    return StegoService(db=db)


# Services injections
def get_role_service(
    db: Session = Depends(get_db),
    repo: RoleRepository = Depends(get_role_repository)
) -> RoleService:
    return RoleService(db, repo)

def get_status_service(
    db: Session = Depends(get_db),
    repo: StatusRepository = Depends(get_status_repository)
) -> StatusService:
    return StatusService(db, repo)

def get_user_status_service(
    db: Session = Depends(get_db),
    repo: UserStatusRepository = Depends(get_user_status_repository)
) -> UserStatusService:
    return UserStatusService(db, repo)

def get_user_role_service(
    db: Session = Depends(get_db),
    repo: UserRoleRepository = Depends(get_user_role_repository)
) -> UserRoleService:
    return UserRoleService(db, repo)

def get_password_history_service(
    db: Session = Depends(get_db),
    repo: PasswordHistoryRepository = Depends(get_password_history_repository)
) -> PasswordHistoryService:
    return PasswordHistoryService(db, repo)

def get_password_reset_token_service(
    db: Session = Depends(get_db),
    repo: PasswordResetTokenRepository = Depends(get_password_reset_token_repository)
) -> PasswordResetTokenRepository:
    return PasswordResetTokenService(db, repo)

def get_user_service(
    db: Session = Depends(get_db),
    user_repo: UserRepository = Depends(get_user_repository),
    status_service: StatusService = Depends(get_status_service),
    user_role_service: UserRoleService = Depends(get_user_role_service),
    user_status_service: UserStatusService = Depends(get_user_status_service)
) -> UserService:
    return UserService( 
        db, 
        user_repo, 
        status_service,
        user_role_service, 
        user_status_service
    )

def get_auth_service(
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
    role_service: RoleService = Depends(get_role_service),
    status_service: StatusService = Depends(get_status_service),
    user_role_service: UserRoleService = Depends(get_user_role_service),
    user_status_service: UserStatusService = Depends(get_user_status_service),
    password_history_service: PasswordHistoryService = Depends(get_password_history_service),
    password_reset_token_service: PasswordResetTokenRepository = Depends(get_password_reset_token_service)
) -> AuthService:
    return AuthService(
        db, 
        user_service, 
        role_service,
        status_service, 
        user_role_service, 
        user_status_service,
        password_history_service,
        password_reset_token_service
    )

def get_google_auth_service(
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
    role_service: RoleService = Depends(get_role_service),
    status_service: StatusService = Depends(get_status_service),
    user_role_service: UserRoleService = Depends(get_user_role_service),
    user_status_service: UserStatusService = Depends(get_user_status_service)
) -> GoogleAuthService:
    return GoogleAuthService(
        db, 
        user_service,
        role_service,
        status_service,
        user_role_service,
        user_status_service
    )


# Authentication dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

def get_current_user(
    request: Request,
    access_token: str = Depends(oauth2_scheme), 
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    # Extract refresh token from request context
    refresh_token = request.cookies.get("refresh_token")

    # Validate refresh and accesstoken
    refresh_token_user = auth_service.validate_token_and_get_user(refresh_token)
    access_token_user = auth_service.validate_token_and_get_user(access_token)
    
    # Ensure both tokens belong to the same user
    if access_token_user.id != refresh_token_user.id:
        raise InvalidCredentialsException()
    
    return access_token_user
from fastapi import Depends
from src.dependencies.injection import get_current_user
from src.exceptions.base_exception import ForbiddenOperationException
from src.schemas.role_schema import RoleEnum
from src.schemas.user_schema import UserRead

def require_roles(*allowed_roles: RoleEnum):
    def _verify(current_user: UserRead = Depends(get_current_user)):
        user_roles = [user_role.role.name for user_role in current_user.roles]
        if not any(role in user_roles for role in allowed_roles):
            raise ForbiddenOperationException("Not enough permissions")
        return current_user
    return _verify

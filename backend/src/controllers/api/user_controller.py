from fastapi import APIRouter, Depends
from src.schemas.base_schema import BaseErrorResponse
from src.dependencies.injection import get_user_service
from src.dependencies.roles import require_roles
from src.schemas.role_schema import RoleEnum
from src.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.delete(
    "/{user_id}/deactivate",
    status_code=204,
    responses={
        204: {"description": "User account deactivated successfully."},
        404: {"model": BaseErrorResponse, "description": "User not found."},
        403: {"model": BaseErrorResponse, "description": "Not enough permissions."},
    },
)
def deactivate_user_account(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    _: None = Depends(require_roles(RoleEnum.ADMIN)),
):
    user_service.deactivate_end_user(user_id)
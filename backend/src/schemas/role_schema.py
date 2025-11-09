from enum import Enum
from pydantic import BaseModel

# NOTE: If you modify RoleEnum, do not forget to update the seeds data accordingly.
class RoleEnum(str, Enum):
    ADMIN = "admin"
    END_USER = "end_user"

class RoleResponse(BaseModel):
    role: RoleEnum
    message: str = ""
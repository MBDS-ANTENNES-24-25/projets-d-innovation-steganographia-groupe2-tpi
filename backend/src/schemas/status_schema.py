from enum import Enum
from pydantic import BaseModel

# NOTE: If you modify StatusEnum, do not forget to update the seeds data accordingly.
class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class StatusResponse(BaseModel):
    status: StatusEnum
    message: str = ""
from pydantic import BaseModel

class BaseMessageResponse(BaseModel):
    msg: str

class BaseErrorResponse(BaseModel):
    err: str

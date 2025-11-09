import re
from pydantic import BaseModel, EmailStr, constr, field_validator
from datetime import datetime

from typing import Annotated
from pydantic import BaseModel, EmailStr, constr

from src.constants.regex_patterns import PASSWORD_REGEX, USERNAME_REGEX


class UserCreate(BaseModel):
    firstname: Annotated[str, constr(strip_whitespace=True, max_length=100)]
    lastname: Annotated[str, constr(strip_whitespace=True, max_length=100)]
    username: Annotated[str, constr(strip_whitespace=True, min_length=3, max_length=50)]
    email: EmailStr
    password: Annotated[str, constr(pattern=PASSWORD_REGEX)]

    @field_validator("firstname")
    @classmethod
    def validate_firstname(cls, v: str) -> str:
        if not v.replace("-", "").replace(" ", "").isalpha():
            raise ValueError("Firstname must contain only letters")
        return v

    @field_validator("lastname")
    @classmethod
    def validate_lastname(cls, v: str) -> str:
        if not v.replace("-", "").replace(" ", "").isalpha():
            raise ValueError("Lastname must contain only letters")
        return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(USERNAME_REGEX, v):
            raise ValueError("Username may only contain letters, numbers, '.', '-', '_'")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.fullmatch(PASSWORD_REGEX, v):
            raise ValueError(
                "Password must be 8-64 characters long and include at least one uppercase letter, "
                "one lowercase letter, one digit, and one special character ( @$!%:;\\/\\_-|~[]{}()*#?& )"
            )
        return v


class UserRead(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

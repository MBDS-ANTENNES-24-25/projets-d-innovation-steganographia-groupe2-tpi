from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="user@yopmail.com")
    password: str = Field(..., example="MyPassword123!")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenRefreshResponse(TokenResponse):
    pass

class TokenPayload(BaseModel):
    sub: int
    exp: int

class EmailConfirmationPayload(BaseModel):
    email: str
    exp: int

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., example="user@yopmail.com")

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
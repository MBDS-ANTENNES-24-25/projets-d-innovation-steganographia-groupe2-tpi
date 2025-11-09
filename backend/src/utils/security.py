from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from src.exceptions.auth_exception import InvalidCredentialsException
from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


def decode_jwt(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.JWTError:
        raise InvalidCredentialsException("Invalid or expired token.")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict):
    expire = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def generate_tokens_for_user(user_id: int):
    payload = {"sub": str(user_id)}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)
    return access_token, refresh_token


def create_email_confirmation_token(email: str):
    expire = datetime.now() + timedelta(minutes=settings.EMAIL_CONFIRMATION_EXPIRE_MINUTES)
    data = {"email": email, "exp": expire}
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
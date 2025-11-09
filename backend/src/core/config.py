from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    GOOGLE_OAUTH2_METADATA_URL: str = "https://accounts.google.com/.well-known/openid-configuration"

    # Admin credentials
    DEFAULT_ADMIN_EMAIL: str = "admin@example.com"
    DEFAULT_ADMIN_PASSWORD: str = "Admin@123"

    # SMTP
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_NAME: str = "Steganographia"

    # Frontend 
    FRONTEND_URL: str
    FRONTEND_RESET_PASSWORD_URL: str
    FRONTEND_CONFIRM_EMAIL_URL: str

    RESET_PASSWORD_EXPIRE_MINUTES: int = 30
    EMAIL_CONFIRMATION_EXPIRE_MINUTES: int = 60
    MAX_PASSWORD_RESET_REQUESTS: int = 1

    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

def get_database_url():
    if not all([settings.POSTGRES_USER, settings.POSTGRES_PASSWORD, settings.POSTGRES_DB]):
        raise ValueError("Database settings are not properly configured.")
    return f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@db:5432/{settings.POSTGRES_DB}"

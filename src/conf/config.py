from pydantic import ConfigDict, EmailStr
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    JWT_SECRET: str
    JWT_ALGO: str = "HS256"
    JWT_EXPIRATION_SECONDS: int = 3600
    
    DB_URL: str = f"postgresql+asyncpg://postgres:567234@postgres:5432/rest_app"
    ALEMBIC_DB_URL: str = f"postgresql+asyncpg://postgres:567234@localhost:5432/rest_app"
    
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    MAIL_USERNAME: EmailStr
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str = "Rest API Service"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    MAIL_TOKEN_EXP_DAYS: int = 7

    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: int
    CLOUDINARY_API_SECRET: str

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

config = Config()

from datetime import timedelta
from typing import Optional
from pydantic_settings import BaseSettings
from secrets import token_urlsafe

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Manager"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str

    # JWT settings
    JWT_SECRET_KEY: str = token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    JWT_ISSUER: str = "fastapi-auth-server"
    JWT_AUDIENCE: str = "fastapi-clients"

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"
        env_file = ".env"

settings = Settings()
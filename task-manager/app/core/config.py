from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Manager"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"
        env_file = ".env"

settings = Settings()
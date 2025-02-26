import secrets
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = "Lunch Decision API"
    
    # Database settings
    DATABASE_URL: PostgresDsn

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
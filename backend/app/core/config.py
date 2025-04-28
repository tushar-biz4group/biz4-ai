"""
Configuration settings for the FastAPI application.
"""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database configuration
    # Using SQLite for simplicity - this doesn't require credentials
    DATABASE_URL: str = "sqlite:///./biz4ai.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/token")

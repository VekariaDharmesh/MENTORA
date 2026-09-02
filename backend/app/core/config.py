"""
Application Configuration & Settings
Manages environment variables, CORS policies, and server metadata.
"""

from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MENTORE Engine API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    # CORS Origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3456",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3456",
        "*"
    ]
    
    # Database & Redis (Optional / Fallback to in-memory)
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ai_teacher_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()

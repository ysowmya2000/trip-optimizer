"""
Application configuration and settings.
Loads environment variables and provides configuration to the app.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App Settings
    APP_NAME: str = "TripOptimizer"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-in-production"
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_PLACES_API_KEY: Optional[str] = None
    GOOGLE_DIRECTIONS_API_KEY: Optional[str] = None
    OPENWEATHER_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "sqlite:///./tripoptimizer.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

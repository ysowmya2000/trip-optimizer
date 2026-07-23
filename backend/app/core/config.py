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

    # Cross-encoder reranking pulls in sentence-transformers, which imports
    # full PyTorch as a side effect regardless of inference backend. That's
    # enough on its own to exceed a 512MB container (measured: OOM-killed
    # under docker run --memory=512m even with no other traffic). The import
    # is lazy (only happens if reranking actually runs), so this flag lets a
    # memory-constrained deployment skip it entirely and fall back to hybrid
    # (BM25+semantic) retrieval without reranking.
    ENABLE_RERANKING: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

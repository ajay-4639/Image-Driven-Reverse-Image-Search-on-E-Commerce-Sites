"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Image Search API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Paths
    DATA_DIR: str = "./data/fashion-images"
    UPLOAD_DIR: str = "./uploads"
    IMAGEBIND_PATH: str = "./ImageBind"

    # Model settings
    DEVICE: str = "cuda"
    EMBEDDING_DIM: int = 1024

    # Qdrant settings
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "imagebind_data"
    USE_IN_MEMORY: bool = True

    # Categories
    PRODUCT_CATEGORIES: List[str] = [
        "Apparel_Boys",
        "Apparel_Girls",
        "Footwear_Men",
        "Footwear_Women"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()

"""
Application configuration using Pydantic settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./hospital.db"

    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-min-32-chars-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    # Storage
    STORAGE_BACKEND: str = "local"  # or "s3"
    UPLOAD_DIR: str = "backend/uploads"
    MAX_UPLOAD_SIZE_MB: int = 50

    # S3 (production only)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET_NAME: Optional[str] = None
    AWS_S3_REGION: str = "us-east-1"
    S3_PRESIGNED_URL_EXPIRY: int = 3600

    # Bootstrap admin
    FIRST_ADMIN_USERNAME: Optional[str] = None
    FIRST_ADMIN_EMAIL: Optional[str] = None
    FIRST_ADMIN_PASSWORD: Optional[str] = None
    FIRST_ADMIN_FULL_NAME: str = "System Administrator"

    # Background tasks
    ENABLE_MEDIA_CLEANUP: bool = True
    MEDIA_CLEANUP_SCHEDULE: str = "0 2 * * *"

    # Logging
    LOG_LEVEL: str = "INFO"

    @property
    def max_upload_size_bytes(self) -> int:
        """Convert MB to bytes for file upload validation."""
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


# Global settings instance
settings = Settings()

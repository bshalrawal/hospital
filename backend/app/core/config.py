from __future__ import annotations

from functools import lru_cache

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration values loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__", case_sensitive=False)

    app_name: str = Field(default="Hospital Equipment Management API", alias="APP_NAME")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=True, alias="DEBUG")

    database_url: AnyUrl | str = Field(
        default="sqlite+aiosqlite:///./hospital.db",
        alias="DATABASE_URL",
        description="SQLAlchemy database URL",
    )

    backend_cors_origins: list[AnyUrl] | str = Field(
        default="http://localhost:3000",
        alias="FRONTEND_URL",
        description="Allowed CORS origins",
    )

    access_token_expire_minutes: int = Field(default=15, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS")
    jwt_secret_key: str = Field(default="change-me", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")

    upload_dir: str = Field(default="backend/uploads", alias="UPLOAD_DIR")
    storage_backend: str = Field(default="local", alias="STORAGE_BACKEND")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings instance."""

    return Settings()


settings = get_settings()

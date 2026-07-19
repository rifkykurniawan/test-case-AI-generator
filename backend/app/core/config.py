import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Test Case AI Generator"
    APP_ENV: Literal["development", "production", "testing"] = "development"
    LOG_LEVEL: str = "INFO"
    GEMINI_API_KEY: str = ""
    MODEL_NAME: str = "gemini-2.0-flash"
    HOST: str = "0.0.0.0"
    PORT: int = 8000


settings = Settings()

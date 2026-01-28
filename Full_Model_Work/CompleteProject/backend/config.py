# config.py (Centralized config & env safety)

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Auth API"

    # Security
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database
    DATABASE_URL: str = "AutoLexis.db"

    # # OpenAI / OCR (NEW)
    # OPENAI_API_KEY: str | None = None
    # TESSERACT_PATH: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"   # allows unused env vars safely


settings = Settings()

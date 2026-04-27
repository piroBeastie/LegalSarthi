"""
LegalSarthi - Configuration
All app settings managed via environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # ── App ──
    APP_NAME: str = "LegalSarthi"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # ── MongoDB ──
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "legalsarthi"

    # ── JWT Auth ──
    SECRET_KEY: str  # Required — set in .env via: python -c "import secrets; print(secrets.token_hex(32))"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # ── Gemini AI ──
    GEMINI_API_KEY: Optional[str] = None  # Set when ready
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"  # Most reliable free tier
    GEMINI_FALLBACK_MODELS: list = [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
    ]
    GEMINI_ENABLED: bool = False  # Flips to True when API key is set
    GEMINI_MAX_RETRIES: int = 2
    GEMINI_RETRY_DELAY: float = 5.0  # seconds

    # ── Rate Limiting ──
    RATE_LIMIT_PER_MINUTE: int = 20

    # ── Future: Multilingual ──
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: list = ["en", "hi"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Auto-enable Gemini if key is present and not empty
if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
    settings.GEMINI_ENABLED = True
else:
    settings.GEMINI_API_KEY = None
    settings.GEMINI_ENABLED = False

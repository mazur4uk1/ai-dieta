from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = Field(default="sqlite:///./ai_dieta.db", env="DATABASE_URL")

    # JWT
    secret_key: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Telegram OAuth
    telegram_bot_token: str = Field(default="your-telegram-bot-token", env="TELEGRAM_BOT_TOKEN")

    # SMS (for development, return code in response)
    sms_api_key: Optional[str] = Field(default=None, env="SMS_API_KEY")

    # Edamam API
    edamam_app_id: Optional[str] = Field(default=None, env="EDAMAM_APP_ID")
    edamam_app_key: Optional[str] = Field(default=None, env="EDAMAM_APP_KEY")

    # App
    app_name: str = "AI-Dieta Backend"
    app_version: str = "1.0.0"
    debug: bool = Field(default=True, env="DEBUG")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

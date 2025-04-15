from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Настройки приложения из .env файла"""
    DATABASE_URL: str = Field(default="sqlite:///./sql_app.db")
    SECRET_KEY: str = Field(default="секретный-ключ")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    class Config:
        env_file = ".env"

# Создаем экземпляр настроек
settings = Settings()
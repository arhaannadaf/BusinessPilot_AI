from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name:str = "BusinessPilot AI"
    app_version: str = "0.1.0"

    DEBUG: bool = True

    host: str = "127.0.0.1"

    port: int = 8000

    DATABASE_URL : str

    secret_key : str

    algorithm : str = "HS256"

    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file= ".env",
        extra="ignore",
    )

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
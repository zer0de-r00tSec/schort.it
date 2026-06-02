from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    admin_url: str = "https://admin.schort.it"
    api_url: str = "https://api.schort.it"
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_DATABASE: str
    BASE_URL: str

    class Config:
        env_file = ".env"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings

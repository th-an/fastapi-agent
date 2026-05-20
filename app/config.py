from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI MongoDB App"
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "myapp"
    LOGFIRE_TOKEN: str | None = None
    ANTHROPIC_API_KEY: str | None = None

    model_config = ConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
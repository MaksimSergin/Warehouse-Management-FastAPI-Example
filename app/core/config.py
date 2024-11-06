from pydantic import Field
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., json_schema_extra={"env": "DATABASE_URL"})
    DATABASE_URL_TEST: str = Field(..., json_schema_extra={"env": "DATABASE_URL_TEST"})
    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"


settings = Settings()

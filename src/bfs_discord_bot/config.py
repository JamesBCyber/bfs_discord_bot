"""Configs read from a .env file"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings from .env, use `settings` instead of creating new class from `Settings`"""

    discord_token: str = Field(validation_alias="discord_token")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

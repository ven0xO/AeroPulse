from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AEROPULSE_",
        env_file=".env",
        env_file_encoding="utf-8",
    )
    app_name: str = "AeroPulse"
    debug: bool = False

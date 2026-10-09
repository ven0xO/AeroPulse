from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AEROPULSE_",
        env_file=".env",
        env_file_encoding="utf-8",
    )
    app_name: str = "AeroPulse"
    debug: bool = False
    db_host: str = "127.0.0.1"
    db_port: int = 5432
    db_name: str = "aeropulse"
    db_user: str = "aeropulse_app"
    db_password: SecretStr

from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    APP_NAME: str = "Amstar"
    URL: MySQLDsn = "mysql+aiomysql://app:password@db:3306/amstar_db"  # type: ignore[assignment]
    POOL_SIZE: int = 10
    CONNECTION_TIMEOUT: int = 15


class APISettings(BaseSettings):
    PUBLIC_PREFIX: str = "/api/app"
    INTERNAL_PREFIX: str = "/api/internal"
    DOCS_ENABLED: bool = True
    DOCS_VERSION: str = "0.1.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8200

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=(".env_defaults", ".env"),
        extra="ignore",
    )

    DB: DatabaseSettings = DatabaseSettings()
    API: APISettings = APISettings()


settings = Settings()

from pathlib import Path

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    DBNAME: str
    DBUSER: str
    DBPASS: str
    DBHOST: str
    DBPORT: int
    DB_DRIVER: str

    DB_POOL_PRE_PING: bool
    DB_POOL_RECYCLE: int
    DB_POOL_SIZE: int
    DB_POOL_OVERFLOW: int

    DEVELOPMENT_LOG_LEVEL: int
    LOG_RAW_SQL_QUERIES: bool
    PROD: bool

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def DATABASE_URI(self) -> str:
        return PostgresDsn.build(
            scheme=f"postgresql+{self.DB_DRIVER}",
            user=self.DBUSER,
            password=self.DBPASS,
            host=self.DBHOST,
            port=str(self.DBPORT),
            path=f"/{self.DBNAME}",
        )


def get_application_settings(file_path: str | Path = None) -> AppSettings:
    if file_path:
        load_dotenv(dotenv_path=file_path)
    else:
        load_dotenv()
    return AppSettings()

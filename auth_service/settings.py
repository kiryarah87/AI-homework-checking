from pathlib import Path

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Класс конфигурации настроек приложения.

    Этот класс определяет настройки для приложения, включая конфигурацию базы данных,
    настройки пула соединений и параметры логирования. Он использует BaseSettings из Pydantic
    для загрузки и валидации переменных окружения.

    Атрибуты:
        DBNAME (str): Имя базы данных
        DBUSER (str): Пользователь базы данных
        DBPASS (str): Пароль базы данных
        DBHOST (str): Хост базы данных
        DBPORT (int): Порт базы данных
        DB_DRIVER (str): Драйвер базы данных (например, 'psycopg2', 'asyncpg')

        DB_POOL_PRE_PING (bool): Включить ли предварительную проверку соединений в пуле
        DB_POOL_RECYCLE (int): Время переиспользования соединений в секундах
        DB_POOL_SIZE (int): Максимальное количество соединений в пуле
        DB_POOL_OVERFLOW (int): Максимальное количество дополнительных соединений

        DEVELOPMENT_LOG_LEVEL (int): Уровень логирования для среды разработки
        LOG_RAW_SQL_QUERIES (bool): Логировать ли сырые SQL-запросы
        PROD (bool): Флаг продакшн-среды

    Свойства:
        DATABASE_URI (str): Сформированный URI подключения к PostgreSQL
    """

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

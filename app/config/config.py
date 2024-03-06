from pydantic_settings import BaseSettings
from pydantic import computed_field
import aiosqlite


class BaseConfig(BaseSettings):
    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"


class AppConfig(BaseConfig):
    DEBUG: bool

    class Config:
        env_prefix = "APP_"


class DataBaseConfig(BaseConfig):
    NAME: str

    @computed_field
    @property
    def postgres_dsn(self) -> str:
        return f"sqlite+{aiosqlite.__name__}:///{self.NAME}.db"

    class Config:
        env_prefix = "DB_"


class Settings(BaseSettings):
    app: AppConfig = AppConfig()
    db: DataBaseConfig = DataBaseConfig()


class Config:
    __config: Settings | None = None

    @classmethod
    def init(cls):
        cls.__config = Settings()

    @classmethod
    def get_config(cls) -> Settings:
        if not cls.__config:
            cls.init()
        return cls.__config

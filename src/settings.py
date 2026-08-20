from functools import lru_cache
from pathlib import Path
from typing import Optional

from sqlalchemy import URL
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    environment: str = "dev"
    api_name: str = "sistema-ponto"

    #JWT
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    #Fernet
    fernet_secret_key: str

    #Database
    database_driver: str
    database_user: Optional[str]
    database_password: Optional[str]
    database_host: Optional[str]
    database_port: Optional[str]
    database_name: str
    database_sslmode: str = "disable"

    database_pool_size: int = 2
    database_pool_max_overflow: int = 6
    database_pool_timeout: int = 10
    database_pool_pre_ping: bool = True
    database_pool_recycle: int = 3600
    database_pool_use_lifo: bool = True

    @property
    def is_sqlite(self) -> bool:
        return "sqlite" in self.database_driver

    @property
    def database_url(self) -> URL:
        if self.is_sqlite:
            return URL.create(
                drivername=self.database_driver,
                database=self.database_name,
            )
        
        return URL.create(
            drivername=self.database_driver,
            username=self.database_user,
            password=self.database_password,
            host=self.database_host,
            port=self.database_port,
            database=self.database_name,
            query={"sslmode": self.database_sslmode},
        )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
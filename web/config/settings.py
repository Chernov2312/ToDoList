__all__ = ()
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    SECRET_KEY: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int = 5432

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=True,
    )

    def get_db_url(self):
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}'
            f':{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}'
            f':{self.POSTGRES_PORT}'
            f'/{self.POSTGRES_DB}'
        )


settings = AppConfig()

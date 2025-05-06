from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class DataBaseSettings(BaseModel):
    user: str
    password: SecretStr
    host: str
    port: int
    database: str
    echo: bool
    pool_size: int
    max_overflow: int

    @property
    def url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.database,
        )


class Settings(BaseSettings):
    db: DataBaseSettings

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )


# noinspection PyArgumentList
settings = Settings()

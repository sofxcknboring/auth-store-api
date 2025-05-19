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


class JwtToken(BaseModel):
    secret: SecretStr
    lifetime_seconds: int


class SuperUser(BaseModel):
    email: str
    password: str


class Settings(BaseSettings):
    db: DataBaseSettings
    jwt_token: JwtToken
    super_user: SuperUser
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )


# noinspection PyArgumentList
settings = Settings()

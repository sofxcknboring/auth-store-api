from fastapi_users.authentication import JWTStrategy
from src.core.config import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.jwt_token.secret,
        lifetime_seconds=settings.jwt_token.lifetime_seconds,
    )

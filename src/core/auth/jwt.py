from fastapi_users.authentication import JWTStrategy
from src.core.config import settings

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.jwt_secret,
        lifetime_seconds=1800 # 30min
    )
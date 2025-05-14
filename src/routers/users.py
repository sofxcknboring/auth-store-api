from fastapi import APIRouter

from src.core.auth.dependencies import fastapi_users
from src.schemas.user import UserRead, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# /me
# /{id}
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))

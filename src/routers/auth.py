from fastapi import APIRouter

from src.core.auth import auth_backend
from src.core.auth.dependencies import fastapi_users
from src.schemas.user import UserRead, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(auth_backend),
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
)

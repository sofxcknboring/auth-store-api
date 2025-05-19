from typing import TYPE_CHECKING
import asyncio
import contextlib

from sqlalchemy import select

from src.core.auth.user_manager import UserManager
from src.core.database import db_helper
from src.routers.dependencies.auth_dependencies import get_user_manager, get_user_db
from src.models.user import User
from src.schemas.user import UserCreate

from src.core.config import settings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


default_email = settings.super_user.email
default_full_name = "full name"
default_phone = "+71234567890"
default_password = settings.super_user.password
default_is_superuser = True
default_is_active = True
default_is_verified = True


async def check_user_exists(session: "AsyncSession", email: str) -> bool:
    """Проверяет существование пользователя по email"""
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none() is not None

async def create_active_user(user_manager: UserManager, user_create: UserCreate) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user

async def create_superuser(
        email: str = default_email,
        password: str = default_password,
        is_superuser: bool = default_is_superuser,
        is_active: bool = default_is_active,
        is_verified: bool = default_is_verified,
        full_name: str = default_full_name,
        phone: str = default_phone
):
    async with db_helper.session_factory() as session:
        if await check_user_exists(session, email):
            return None

    user_create = UserCreate(
        full_name=full_name,
        phone=phone,
        email=email,
        password=password,
        is_superuser=is_superuser,
        is_active=is_active,
        is_verified=is_verified,
    )
    async with db_helper.session_factory() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                return await create_active_user(user_manager, user_create)

if __name__ == "__main__":
    asyncio.run(create_superuser())
from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi_users import FastAPIUsers

from src.models.user import User
from . import auth_backend
from .user_manager import UserManager
from ..database import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_db(session: "AsyncSession" = Depends(db_helper.session_getter)):
    yield User.get_db(session=session)


async def get_user_manager(user_db: "SQLAlchemyUserDatabase" = Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_super_user = fastapi_users.current_user(active=True, superuser=True)

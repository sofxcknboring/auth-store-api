from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, SQLAlchemyBaseUserTable[int]):

    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), unique=True, index=True, nullable=False)

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)
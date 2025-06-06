import logging
import re
from typing import Optional, TYPE_CHECKING
from fastapi import HTTPException

from fastapi_users import IntegerIDMixin, BaseUserManager

from src.core.database import db_helper
from src.models import Cart
from src.models.user import User

from src.core.config import settings

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.jwt_token.secret
    verification_token_secret = settings.jwt_token.secret

    async def validate_password(self, password: str, user: User) -> None:
        if len(password) < 8:
            raise HTTPException(
                status_code=400, detail="Password must be at least 8 characters long"
            )
        if not re.match(r"^[A-Za-z0-9$%&!:]+$", password):
            raise HTTPException(
                status_code=400,
                detail="Password can only contain Latin letters, numbers and special characters $%&!:",
            )
        if not re.search(r"[A-Z]", password):
            raise HTTPException(
                status_code=400,
                detail="Password must contain at least 1 uppercase letter",
            )
        if not re.search(r"[$%&!:]", password):
            raise HTTPException(
                status_code=400,
                detail="Password must contain at least 1 special character ($%&!:)",
            )
        await super().validate_password(password, user)

    async def on_after_register(
        self, user: User, request: Optional["Request"] = None
    ) -> None:
        log.warning(f"User {user.id} has registered.")

        # Create Cart for current user before register
        async with db_helper.session_factory() as session:
            async with session.begin():
                cart = Cart(user_id=user.id)
                session.add(cart)
                log.warning(f"Cart created for user {user.id}")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional["Request"] = None
    ) -> None:
        # Some logic
        log.warning(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional["Request"] = None
    ) -> None:
        # Some logic
        log.warning(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )

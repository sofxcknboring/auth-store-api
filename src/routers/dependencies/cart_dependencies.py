from typing import TYPE_CHECKING
from fastapi import Depends, HTTPException

from src.core.database import db_helper
from src.models import User
from src.models.cart import Cart
from src.routers.dependencies.auth_dependencies import current_active_user
from src.services.cart import get_cart_by_user_id

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_cart(
    user: User = Depends(current_active_user),
    session: "AsyncSession" = Depends(db_helper.session_getter),
) -> Cart:
    user_cart = await get_cart_by_user_id(user_id=user.id, session=session)
    if user_cart is not None:
        return user_cart
    raise HTTPException(status_code=404, detail=f"Cart for user {user.id} not found")

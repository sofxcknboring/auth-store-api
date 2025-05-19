from typing import TYPE_CHECKING

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from src.models import Cart, CartItem, Product
from src.schemas.cart import CartItemAdd, CartItemUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_cart_by_user_id(session: "AsyncSession", user_id: int) -> Cart:
    stmt = (
        select(Cart)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
        .where(Cart.user_id == user_id)
    )
    result = await session.execute(stmt)
    cart = result.scalar_one()

    return cart


async def add_item_to_cart(
    session: "AsyncSession", cart: Cart, product: Product, item_data: CartItemAdd
) -> CartItem:

    item = next(
        (item for item in cart.items if item.product_id == product.id),
        None,
    )

    if item:
        item.quantity += item_data.quantity

    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=item_data.quantity,
        )
        session.add(item)

    await session.commit()
    await session.refresh(product)
    return item


async def update_item_in_cart(
    session: "AsyncSession",
    cart: Cart,
    product: Product,
    quantity_update: CartItemUpdate,
) -> CartItem:

    item = next(
        (item for item in cart.items if item.product_id == product.id),
        None,
    )
    if item:
        item.quantity = quantity_update.quantity
        await session.commit()
        await session.refresh(item)
        return item
    return None


async def delete_item_from_cart(
    session: "AsyncSession",
    cart: Cart,
    product: Product,
):
    item = next(
        (item for item in cart.items if item.product_id == product.id),
        None,
    )
    await session.delete(item)
    await session.commit()


async def clear_cart_items(
    session: "AsyncSession",
    cart: Cart,
):
    await session.execute(delete(CartItem).where(CartItem.cart_id == cart.id))
    await session.commit()

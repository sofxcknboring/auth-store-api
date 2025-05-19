from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, status, HTTPException

from src.models import Product, Cart

from src.schemas.cart import CartResponse, CartItemResponse, CartItemAdd, CartItemUpdate

from src.core.database import db_helper

from src.routers.dependencies.product_dependencies import get_product_by_id
from src.routers.dependencies.auth_dependencies import current_active_user
from src.routers.dependencies.cart_dependencies import get_user_cart

from src.services.cart import (
    add_item_to_cart,
    update_item_in_cart,
    delete_item_from_cart, clear_cart_items,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/cart", tags=["Cart"], dependencies=[Depends(current_active_user)]
)


# Эндпоинты
@router.get("/", response_model=CartResponse)
async def get_cart(cart: Cart = Depends(get_user_cart)):
    return cart


@router.post(
    "/items/{product_id}/",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_item(
    item_data: CartItemAdd,
    cart: Cart = Depends(get_user_cart),
    product: Product = Depends(get_product_by_id),
    session: "AsyncSession" = Depends(db_helper.session_getter),
):
    cart_response = await add_item_to_cart(
        session=session, cart=cart, product=product, item_data=item_data
    )
    return cart_response


@router.patch("/items/{product_id}", response_model=CartItemResponse)
async def update_item(
    quantity_update: CartItemUpdate,
    product: Product = Depends(get_product_by_id),
    cart: Cart = Depends(get_user_cart),
    session: "AsyncSession" = Depends(db_helper.session_getter),
):
    updated_item = await update_item_in_cart(
        session=session, cart=cart, product=product, quantity_update=quantity_update
    )

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated_item


@router.delete("/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item(
    product: Product = Depends(get_product_by_id),
    cart: Cart = Depends(get_user_cart),
    session: "AsyncSession" = Depends(db_helper.session_getter),
):
    await delete_item_from_cart(
        session=session,
        cart=cart,
        product=product,
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    cart: Cart = Depends(get_user_cart),
    session: "AsyncSession" = Depends(db_helper.session_getter),
):
    await clear_cart_items(
        session=session,
        cart=cart,
    )

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, status

from src.models import Product
from src.services import product_crud
from src.schemas.product import ProductCreate, ProductResponse, ProductUpdatePartial
from src.core.database import db_helper

from src.routers.dependencies.auth_dependencies import current_super_user
from src.routers.dependencies.product_dependencies import get_product_by_id


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/products", tags=["Products"], dependencies=[Depends(current_super_user)]
)


@router.get("/", response_model=list[ProductResponse])
async def get_products(session: "AsyncSession" = Depends(db_helper.session_getter)):
    return await product_crud.get_products(session)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    session: "AsyncSession" = Depends(db_helper.session_getter),
):
    return await product_crud.create_product(session, product_in)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product: Product = Depends(get_product_by_id),
):
    return product


@router.patch("/{product_id}/", response_model=ProductResponse)
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(get_product_by_id),
    session: "AsyncSession" = Depends(db_helper.session_getter),
):
    return await product_crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(get_product_by_id),
    session: "AsyncSession" = Depends(db_helper.session_getter),
):
    await product_crud.delete_product(session, product)

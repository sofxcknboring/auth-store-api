from typing import TYPE_CHECKING, Optional
from src.models.product import Product
from sqlalchemy import select
from sqlalchemy.engine import Result

from src.schemas.product import ProductCreate, ProductUpdate, ProductUpdatePartial

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_products(session: "AsyncSession") -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(session: "AsyncSession", product_id: int) -> Optional[Product]:
    return await session.get(Product, product_id)


async def create_product(session: "AsyncSession", product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def update_product(
    session: "AsyncSession",
    product: Product,
    product_update: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> Product:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    await session.refresh(product)  # чтобы корректно вернуть поле updated_at
    return product


async def delete_product(session: "AsyncSession", product: Product) -> None:
    await session.delete(product)
    await session.commit()

from typing import TYPE_CHECKING

from fastapi import Path, Depends, HTTPException

from typing import Annotated

from src.core.database import db_helper
from src.models import Product
from src.services import product_crud

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_product_by_id(
    product_id: Annotated[int, Path],
    session: "AsyncSession" = Depends(db_helper.session_getter),
) -> Product:
    product = await product_crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

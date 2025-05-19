from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from src.core.database import db_helper

from src.routers.auth import router as auth_router
from src.routers.users import router as users_router
from src.routers.products import router as products_router
from src.routers.cart import router as cart_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    yield
    # end
    await db_helper.dispose()

http_bearer = HTTPBearer(auto_error=False)
main_app = FastAPI(
    default_response_class=JSONResponse,
    lifespan=lifespan,
    dependencies=[Depends(http_bearer)],
)
main_app.include_router(auth_router)
main_app.include_router(users_router)
main_app.include_router(products_router)
main_app.include_router(cart_router)


if __name__ == "__main__":
    uvicorn.run(main_app, host="0.0.0.0", port=8000)
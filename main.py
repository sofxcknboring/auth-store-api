from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.core.database import db_helper

from src.routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    yield
    # end
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=JSONResponse,
    lifespan=lifespan,
)
main_app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(main_app, host="0.0.0.0", port=8000)
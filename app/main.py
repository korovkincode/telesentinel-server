from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.api.exc_handler as app_exc_handler
from app.api.router import router
from app.core.db import AsyncSessionLocal
from app.core.init_superuser import init_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as session:
        await init_superuser(session)
        yield


app = FastAPI(lifespan=lifespan, title="TeleSentinel-Server")
app.include_router(router, prefix="/api")
app_exc_handler.register_exc_handlers(app)

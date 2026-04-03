from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db import AsyncSessionLocal
from app.core.init_superuser import init_superuser
from app.api.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as session:
        await init_superuser(session)
        yield


app = FastAPI(lifespan=lifespan, title="TeleSentinel-Server")
app.include_router(router, prefix="/api")

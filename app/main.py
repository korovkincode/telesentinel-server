from contextlib import asynccontextmanager

from fastapi import FastAPI
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

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

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])
app.include_router(router)
app_exc_handler.register_exc_handlers(app)

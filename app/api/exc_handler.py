from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exc.base import AppError


def register_exc_handlers(app: FastAPI):
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code,
                "message": exc.message,
                "details": exc.context,
            },
        )

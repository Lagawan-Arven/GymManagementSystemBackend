# core/exception_handlers.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from core.exceptions import AppException
import traceback,logging

logger = logging.getLogger(__name__)

def add_exception_handlers(app: FastAPI):

    # ====================================
    # 🔹 Custom App Exceptions
    # ====================================
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "details": exc.details,
                },
            },
        )

    # ====================================
    # 🔹 Validation Errors (Pydantic)
    # ====================================
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Validation failed",
                    "details": exc.errors(),
                },
            },
        )

    # ====================================
    # 🔹 Rate Limiting
    # ====================================
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests",
                },
            },
        )

    # ====================================
    # 🔥 Fallback Global Error
    # ====================================
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):

        logging.error('Unhandled errors')
        # Optional: log full traceback
        print("UNHANDLED ERROR:")
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Something went wrong",
                },
            },
        )

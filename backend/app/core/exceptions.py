from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger


class AppError(Exception):
    """Base application exception."""

    def __init__(
        self, message: str, status_code: int = 500, detail: dict | None = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}


class RequirementValidationError(AppError):
    """Error raised when requirements fail validation."""

    def __init__(self, message: str, detail: dict | None = None):
        super().__init__(message, status_code=400, detail=detail)


class AIProviderError(AppError):
    """Error raised when external AI provider fails."""

    def __init__(self, message: str, detail: dict | None = None):
        super().__init__(message, status_code=502, detail=detail)


class ExportError(AppError):
    """Error raised when export service fails."""

    def __init__(self, message: str, detail: dict | None = None):
        super().__init__(message, status_code=500, detail=detail)


def setup_exception_handlers(app: FastAPI) -> None:
    """Register application exception handlers."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        logger.error(
            "Application error occurred: {} (Status: {}) | Detail: {}",
            exc.message,
            exc.status_code,
            exc.detail,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "type": exc.__class__.__name__,
                    "message": exc.message,
                    "detail": exc.detail,
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled exception occurred: {}", str(exc))
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": "UnhandledError",
                    "message": "An unexpected error occurred on the server.",
                    "detail": {"message": str(exc)} if app.debug else {},
                }
            },
        )

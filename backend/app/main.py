import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api import export, generate, health
from app.core.config import settings
from app.core.exceptions import setup_exception_handlers
from app.core.logger import configure_logging

# Initialize Logger
configure_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend foundation for generating structured test cases using LLMs.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Centralized exception handling
setup_exception_handlers(app)


# Logging Middleware to record request/response cycles and processing times
@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    path = request.url.path
    method = request.method

    logger.info("Incoming request: {} {}", method, path)

    try:
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        logger.info(
            "Request finished: {} {} | Status: {} | Duration: {:.4f}s",
            method,
            path,
            response.status_code,
            process_time,
        )
        return response
    except Exception as e:
        process_time = time.perf_counter() - start_time
        logger.error(
            "Request failed: {} {} | Duration: {:.4f}s | Error: {}",
            method,
            path,
            process_time,
            str(e),
        )
        raise e


# Include Routers
app.include_router(health.router)
app.include_router(generate.router)
app.include_router(export.router)

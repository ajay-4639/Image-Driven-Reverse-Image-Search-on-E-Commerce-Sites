"""
FastAPI application entry point.
"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import settings
from .core.logging import logger
from .api.router import api_router
from .services.search_service import search_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Image Search API...")
    logger.info(f"Device: {settings.DEVICE}")
    logger.info(f"Data directory: {settings.DATA_DIR}")

    # Initialize search service in background
    asyncio.create_task(initialize_services())

    yield

    # Shutdown
    logger.info("Shutting down Image Search API...")


async def initialize_services():
    """Initialize all services asynchronously."""
    try:
        await search_service.initialize()
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
## Image-Driven Reverse Image Search API

A powerful API for performing reverse image search on e-commerce products
using Meta's ImageBind model and Qdrant vector database.

### Features

- **Reverse Image Search**: Upload an image to find similar products
- **Category Browsing**: Browse products by category
- **High Performance**: GPU-accelerated embeddings with vector similarity search

### Categories

- Apparel Boys
- Apparel Girls
- Footwear Men
- Footwear Women
        """,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router)

    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": "/api/v1/health"
        }

    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

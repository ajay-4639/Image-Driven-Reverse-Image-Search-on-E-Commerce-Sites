"""
API router aggregating all route modules.
"""
from fastapi import APIRouter

from .routes import health, search, categories, images

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Include all route modules
api_router.include_router(health.router)
api_router.include_router(search.router)
api_router.include_router(categories.router)
api_router.include_router(images.router)

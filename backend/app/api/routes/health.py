"""
Health check API routes.
"""
from fastapi import APIRouter
from datetime import datetime

from ...models.schemas import HealthResponse, IndexingStatus
from ...services.search_service import search_service

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
async def health_check():
    """
    Check the health status of the API.

    Returns service status including model and database connectivity.
    """
    health_info = search_service.get_health_info()

    return HealthResponse(
        status="healthy" if health_info["initialized"] else "initializing",
        model_loaded=health_info["model_loaded"],
        vector_db_connected=health_info["vector_db_connected"],
        indexed_images=health_info["indexed_images"],
        timestamp=datetime.utcnow()
    )


@router.get("/ready")
async def readiness_check():
    """
    Check if the service is ready to accept requests.
    """
    health_info = search_service.get_health_info()

    if health_info["initialized"]:
        return {"status": "ready"}
    return {"status": "not_ready", "message": "Service is still initializing"}


@router.get("/live")
async def liveness_check():
    """
    Check if the service is alive.
    """
    return {"status": "alive"}


@router.get("/indexing", response_model=IndexingStatus)
async def get_indexing_status():
    """
    Get the current indexing status.
    """
    status = search_service.get_indexing_status()

    return IndexingStatus(
        is_indexing=status["is_indexing"],
        total_images=status["total_images"],
        indexed_images=status["indexed_images"],
        current_category=status.get("current_category"),
        progress_percentage=status["progress_percentage"]
    )

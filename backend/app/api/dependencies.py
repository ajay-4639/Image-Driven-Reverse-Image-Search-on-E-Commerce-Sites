"""
API dependencies for dependency injection.
"""
from fastapi import Depends, HTTPException, status

from ..services.search_service import search_service
from ..services.embedding_service import embedding_service
from ..services.vector_store import vector_store
from ..core.exceptions import ModelNotLoadedException


async def get_search_service():
    """
    Dependency that provides the search service.
    Raises 503 if service is not initialized.
    """
    if not search_service.is_initialized:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is initializing. Please try again later."
        )
    return search_service


async def get_embedding_service():
    """
    Dependency that provides the embedding service.
    Raises 503 if model is not loaded.
    """
    if not embedding_service.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Please try again later."
        )
    return embedding_service


async def get_vector_store():
    """
    Dependency that provides the vector store.
    Raises 503 if not connected.
    """
    if not vector_store.is_connected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Vector database is not connected. Please try again later."
        )
    return vector_store

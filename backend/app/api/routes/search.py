"""
Image search API routes.
"""
import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import Optional

from ...models.schemas import SearchResponse, ErrorResponse
from ...services.search_service import search_service
from ...services.image_processor import image_processor
from ...core.logging import logger
from ...core.exceptions import (
    ModelNotLoadedException,
    ImageProcessingException
)

router = APIRouter(prefix="/search", tags=["Search"])


@router.post(
    "",
    response_model=SearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid image"},
        500: {"model": ErrorResponse, "description": "Search failed"},
        503: {"model": ErrorResponse, "description": "Service not ready"}
    }
)
async def search_similar_images(
    image: UploadFile = File(..., description="Image file to search for"),
    limit: int = 5
):
    """
    Search for similar images using an uploaded image.

    Upload an image and get the most similar product images from the database.

    - **image**: Image file (PNG, JPG, JPEG, GIF, BMP, WebP)
    - **limit**: Maximum number of results to return (1-20)
    """
    # Validate file type
    if not image.filename or not image_processor.is_valid_image(image.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file. Supported formats: PNG, JPG, JPEG, GIF, BMP, WebP"
        )

    # Limit validation
    if limit < 1 or limit > 20:
        limit = min(max(limit, 1), 20)

    temp_path = None
    try:
        # Save uploaded file temporarily
        content = await image.read()
        temp_path = await image_processor.save_upload(content, image.filename)

        # Perform search
        result = await search_service.search_by_image(temp_path, limit=limit)
        return result

    except ModelNotLoadedException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except ImageProcessingException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
    finally:
        # Cleanup temp file
        if temp_path:
            image_processor.cleanup_upload(temp_path)


@router.post(
    "/url",
    response_model=SearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid URL"},
        500: {"model": ErrorResponse, "description": "Search failed"}
    }
)
async def search_by_url(
    image_url: str,
    limit: int = 5
):
    """
    Search for similar images using an image URL.

    Note: This endpoint requires the image to be accessible from the server.

    - **image_url**: URL of the image to search for
    - **limit**: Maximum number of results to return (1-20)
    """
    # For now, return a not implemented error
    # In production, you would download the image and process it
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="URL-based search not yet implemented. Please use file upload."
    )

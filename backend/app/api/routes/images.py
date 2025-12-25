"""
Image serving API routes.
"""
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import FileResponse

from ...core.logging import logger
from ...services.image_processor import image_processor

router = APIRouter(prefix="/images", tags=["Images"])


@router.get(
    "/file",
    response_class=FileResponse,
    summary="Get image file"
)
async def get_image_file(
    path: str = Query(..., description="Path to the image file")
):
    """
    Serve an image file by its path.

    - **path**: Full path to the image file
    """
    # Security check: ensure path doesn't escape allowed directories
    resolved_path = Path(path).resolve()

    # Check if file exists
    if not resolved_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    # Validate it's an image
    if not image_processor.is_valid_image(str(resolved_path)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file"
        )

    # Determine media type
    suffix = resolved_path.suffix.lower()
    media_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".bmp": "image/bmp",
        ".webp": "image/webp"
    }
    media_type = media_types.get(suffix, "image/jpeg")

    return FileResponse(
        path=str(resolved_path),
        media_type=media_type,
        filename=resolved_path.name
    )


@router.get(
    "/info",
    summary="Get image information"
)
async def get_image_info(
    path: str = Query(..., description="Path to the image file")
):
    """
    Get metadata about an image file.

    - **path**: Full path to the image file
    """
    try:
        info = image_processor.get_image_info(path)
        return info
    except Exception as e:
        logger.error(f"Error getting image info: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found or could not be read"
        )

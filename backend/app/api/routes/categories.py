"""
Category API routes.
"""
from fastapi import APIRouter, HTTPException, Query, status

from ...models.schemas import (
    CategoryResponse,
    CategoriesResponse,
    CategoryInfo,
    ErrorResponse
)
from ...services.search_service import search_service
from ...core.exceptions import CategoryNotFoundException
from ...core.logging import logger

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get(
    "",
    response_model=CategoriesResponse,
    summary="Get all categories"
)
async def get_categories():
    """
    Get a list of all available product categories.

    Returns category names, display names, and image counts.
    """
    categories = search_service.get_all_categories()
    return CategoriesResponse(categories=categories)


@router.get(
    "/{category}",
    response_model=CategoryResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Category not found"}
    },
    summary="Get category images"
)
async def get_category_images(
    category: str,
    limit: int = Query(default=10, ge=1, le=50, description="Number of images to return"),
    random: bool = Query(default=False, description="Return random images")
):
    """
    Get images from a specific category.

    - **category**: Category name (e.g., "Apparel_Boys", "Footwear_Men")
    - **limit**: Maximum number of images to return
    - **random**: If true, returns random images from the category
    """
    try:
        result = search_service.get_category_images(
            category=category,
            limit=limit,
            random_sample=random
        )
        return result

    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.message)
        )
    except Exception as e:
        logger.error(f"Error getting category images: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve category images"
        )


@router.get(
    "/{category}/random",
    response_model=CategoryResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Category not found"}
    },
    summary="Get random category images"
)
async def get_random_category_images(
    category: str,
    count: int = Query(default=1, ge=1, le=20, description="Number of random images")
):
    """
    Get random images from a specific category.

    - **category**: Category name
    - **count**: Number of random images to return
    """
    try:
        result = search_service.get_category_images(
            category=category,
            limit=count,
            random_sample=True
        )
        return result

    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.message)
        )
    except Exception as e:
        logger.error(f"Error getting random category images: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve random images"
        )

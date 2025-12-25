"""
Pydantic schemas for API request/response models.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# ============ Request Schemas ============

class SearchRequest(BaseModel):
    """Request schema for image search by URL."""
    image_url: str = Field(..., description="URL of the image to search")
    limit: int = Field(default=5, ge=1, le=20, description="Number of results to return")


class CategoryRequest(BaseModel):
    """Request schema for category-based search."""
    category: str = Field(..., description="Product category name")
    limit: int = Field(default=10, ge=1, le=50, description="Number of images to return")
    random: bool = Field(default=False, description="Whether to return random images")


# ============ Response Schemas ============

class ImageResult(BaseModel):
    """Single image result."""
    id: str = Field(..., description="Unique identifier for the image")
    path: str = Field(..., description="Path to the image file")
    url: str = Field(..., description="URL to access the image")
    score: Optional[float] = Field(None, description="Similarity score (0-1)")
    category: Optional[str] = Field(None, description="Product category")


class SearchResponse(BaseModel):
    """Response schema for image search results."""
    query_image: Optional[str] = Field(None, description="Query image identifier")
    results: List[ImageResult] = Field(default_factory=list, description="List of matching images")
    total: int = Field(..., description="Total number of results")
    search_time_ms: float = Field(..., description="Search time in milliseconds")


class CategoryResponse(BaseModel):
    """Response schema for category images."""
    category: str = Field(..., description="Category name")
    images: List[ImageResult] = Field(default_factory=list, description="List of images")
    total: int = Field(..., description="Total images in category")


class CategoryInfo(BaseModel):
    """Information about a product category."""
    name: str = Field(..., description="Category name")
    display_name: str = Field(..., description="Human-readable category name")
    image_count: int = Field(..., description="Number of images in category")


class CategoriesResponse(BaseModel):
    """Response schema for all categories."""
    categories: List[CategoryInfo] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether the ML model is loaded")
    vector_db_connected: bool = Field(..., description="Whether vector DB is connected")
    indexed_images: int = Field(..., description="Number of indexed images")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class IndexingStatus(BaseModel):
    """Status of the indexing process."""
    is_indexing: bool = Field(..., description="Whether indexing is in progress")
    total_images: int = Field(..., description="Total images to index")
    indexed_images: int = Field(..., description="Number of indexed images")
    current_category: Optional[str] = Field(None, description="Category being indexed")
    progress_percentage: float = Field(..., description="Indexing progress percentage")


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")

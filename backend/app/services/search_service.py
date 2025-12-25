"""
Search service for coordinating image search operations.
"""
import os
import time
import random
import asyncio
from typing import List, Optional
from pathlib import Path

from ..core.config import settings
from ..core.logging import logger
from ..core.exceptions import (
    CategoryNotFoundException,
    ImageProcessingException,
    ModelNotLoadedException
)
from ..models.schemas import ImageResult, SearchResponse, CategoryResponse, CategoryInfo
from .image_processor import image_processor
from .embedding_service import embedding_service
from .vector_store import vector_store


class SearchService:
    """Service for coordinating image search operations."""

    def __init__(self):
        self.is_initialized = False
        self.indexing_status = {
            "is_indexing": False,
            "total_images": 0,
            "indexed_images": 0,
            "current_category": None
        }

    async def initialize(self) -> None:
        """Initialize all services and index images."""
        if self.is_initialized:
            logger.info("Search service already initialized")
            return

        try:
            # Load embedding model
            logger.info("Initializing embedding service...")
            embedding_service.load_model()

            # Connect to vector store
            logger.info("Connecting to vector store...")
            vector_store.connect()

            # Index images
            await self.index_all_images()

            self.is_initialized = True
            logger.info("Search service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize search service: {e}")
            raise

    async def index_all_images(self) -> int:
        """
        Index all images from all categories.

        Returns:
            Total number of indexed images
        """
        self.indexing_status["is_indexing"] = True
        total_indexed = 0

        try:
            all_paths = image_processor.get_all_image_paths()
            total_images = sum(len(paths) for paths in all_paths.values())
            self.indexing_status["total_images"] = total_images

            for category, paths in all_paths.items():
                if not paths:
                    continue

                self.indexing_status["current_category"] = category
                logger.info(f"Indexing {len(paths)} images from {category}")

                # Generate embeddings in batches
                batch_size = 32
                for i in range(0, len(paths), batch_size):
                    batch_paths = paths[i:i + batch_size]

                    # Generate embeddings
                    embeddings = embedding_service.generate_embeddings_batch(batch_paths)

                    # Store in vector database
                    vector_store.upsert_embeddings(embeddings, batch_paths)

                    total_indexed += len(batch_paths)
                    self.indexing_status["indexed_images"] = total_indexed

                    # Yield control to allow other operations
                    await asyncio.sleep(0)

            logger.info(f"Indexed {total_indexed} images total")
            return total_indexed

        finally:
            self.indexing_status["is_indexing"] = False
            self.indexing_status["current_category"] = None

    async def search_by_image(
        self,
        image_path: str,
        limit: int = 5
    ) -> SearchResponse:
        """
        Search for similar images given an image path.

        Args:
            image_path: Path to the query image
            limit: Number of results to return

        Returns:
            SearchResponse with matching images
        """
        if not self.is_initialized:
            raise ModelNotLoadedException("Search service not initialized")

        start_time = time.time()

        try:
            # Generate embedding for query image
            query_embedding = embedding_service.generate_embedding(image_path)

            # Search in vector store
            results = vector_store.search(query_embedding, limit=limit)

            # Build response
            image_results = []
            for path, score in results:
                category = image_processor.get_category_from_path(path)
                image_results.append(
                    ImageResult(
                        id=Path(path).stem,
                        path=path,
                        url=f"/api/v1/images/file?path={path}",
                        score=score,
                        category=category
                    )
                )

            search_time = (time.time() - start_time) * 1000

            return SearchResponse(
                query_image=image_path,
                results=image_results,
                total=len(image_results),
                search_time_ms=round(search_time, 2)
            )

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise ImageProcessingException(f"Search failed: {str(e)}")

    def get_category_images(
        self,
        category: str,
        limit: int = 10,
        random_sample: bool = False
    ) -> CategoryResponse:
        """
        Get images from a specific category.

        Args:
            category: Category name
            limit: Number of images to return
            random_sample: Whether to return random images

        Returns:
            CategoryResponse with images
        """
        # Normalize category name
        normalized_category = category.replace(" ", "_")

        # Check if category exists
        if normalized_category not in settings.PRODUCT_CATEGORIES:
            raise CategoryNotFoundException(category)

        # Get image paths
        paths = image_processor.get_image_paths_for_category(normalized_category)

        if not paths:
            raise CategoryNotFoundException(category)

        # Sample images
        if random_sample and len(paths) > limit:
            selected_paths = random.sample(paths, limit)
        else:
            selected_paths = paths[:limit]

        # Build response
        image_results = [
            ImageResult(
                id=Path(path).stem,
                path=path,
                url=f"/api/v1/images/file?path={path}",
                category=normalized_category
            )
            for path in selected_paths
        ]

        return CategoryResponse(
            category=normalized_category,
            images=image_results,
            total=len(paths)
        )

    def get_all_categories(self) -> List[CategoryInfo]:
        """Get information about all categories."""
        categories = []
        all_paths = image_processor.get_all_image_paths()

        for category in settings.PRODUCT_CATEGORIES:
            display_name = category.replace("_", " ")
            image_count = len(all_paths.get(category, []))

            categories.append(
                CategoryInfo(
                    name=category,
                    display_name=display_name,
                    image_count=image_count
                )
            )

        return categories

    def get_indexing_status(self) -> dict:
        """Get current indexing status."""
        status = self.indexing_status.copy()
        if status["total_images"] > 0:
            status["progress_percentage"] = round(
                (status["indexed_images"] / status["total_images"]) * 100, 2
            )
        else:
            status["progress_percentage"] = 0
        return status

    def get_health_info(self) -> dict:
        """Get health information about the service."""
        collection_info = vector_store.get_collection_info()
        model_info = embedding_service.get_model_info()

        return {
            "initialized": self.is_initialized,
            "model_loaded": model_info.get("loaded", False),
            "vector_db_connected": collection_info.get("connected", False),
            "indexed_images": collection_info.get("vectors_count", 0),
            "device": model_info.get("device", "unknown")
        }


# Singleton instance
search_service = SearchService()

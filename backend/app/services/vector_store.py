"""
Vector store service for managing embeddings in Qdrant.
"""
import uuid
from typing import List, Optional, Tuple
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct

from ..core.config import settings
from ..core.logging import logger
from ..core.exceptions import VectorDatabaseException


class VectorStore:
    """Service for managing vector embeddings in Qdrant."""

    def __init__(self):
        self.client: Optional[QdrantClient] = None
        self.collection_name = settings.QDRANT_COLLECTION
        self.is_connected = False
        self.indexed_count = 0

    def connect(self) -> None:
        """Initialize connection to Qdrant."""
        try:
            if settings.USE_IN_MEMORY:
                self.client = QdrantClient(":memory:")
                logger.info("Connected to in-memory Qdrant instance")
            else:
                self.client = QdrantClient(
                    host=settings.QDRANT_HOST,
                    port=settings.QDRANT_PORT
                )
                logger.info(f"Connected to Qdrant at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")

            self._create_collection()
            self.is_connected = True

        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise VectorDatabaseException(f"Failed to connect to vector database: {str(e)}")

    def _create_collection(self) -> None:
        """Create or recreate the vector collection."""
        try:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "image": VectorParams(
                        size=settings.EMBEDDING_DIM,
                        distance=Distance.COSINE
                    )
                }
            )
            logger.info(f"Created collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise VectorDatabaseException(f"Failed to create collection: {str(e)}")

    def upsert_embeddings(
        self,
        embeddings: List[List[float]],
        image_paths: List[str],
        batch_size: int = 100
    ) -> int:
        """
        Insert or update embeddings in the vector store.

        Args:
            embeddings: List of embedding vectors
            image_paths: Corresponding image paths
            batch_size: Number of points to upsert at once

        Returns:
            Number of points upserted
        """
        if not self.is_connected:
            raise VectorDatabaseException("Not connected to vector database")

        try:
            points = []
            for embedding, path in zip(embeddings, image_paths):
                point_id = str(uuid.uuid4())
                points.append(
                    PointStruct(
                        id=point_id,
                        vector={"image": embedding},
                        payload={"path": path}
                    )
                )

            # Batch upsert
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )

            self.indexed_count += len(points)
            logger.info(f"Upserted {len(points)} embeddings")
            return len(points)

        except Exception as e:
            logger.error(f"Failed to upsert embeddings: {e}")
            raise VectorDatabaseException(f"Failed to upsert embeddings: {str(e)}")

    def search(
        self,
        query_embedding: List[float],
        limit: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Search for similar images.

        Args:
            query_embedding: Query embedding vector
            limit: Number of results to return

        Returns:
            List of (image_path, score) tuples
        """
        if not self.is_connected:
            raise VectorDatabaseException("Not connected to vector database")

        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=models.NamedVector(
                    name="image",
                    vector=query_embedding
                ),
                limit=limit
            )

            return [
                (hit.payload.get("path", ""), hit.score)
                for hit in results
                if hit.payload
            ]

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise VectorDatabaseException(f"Search failed: {str(e)}")

    def get_collection_info(self) -> dict:
        """Get information about the collection."""
        if not self.is_connected:
            return {"connected": False}

        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "connected": True,
                "collection_name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status.value
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {"connected": True, "error": str(e)}

    def delete_all(self) -> None:
        """Delete all points from the collection."""
        if not self.is_connected:
            raise VectorDatabaseException("Not connected to vector database")

        try:
            self._create_collection()
            self.indexed_count = 0
            logger.info("Deleted all points from collection")
        except Exception as e:
            logger.error(f"Failed to delete points: {e}")
            raise VectorDatabaseException(f"Failed to delete points: {str(e)}")


# Singleton instance
vector_store = VectorStore()

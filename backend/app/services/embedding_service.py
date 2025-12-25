"""
Embedding service for generating image embeddings using ImageBind.
"""
import sys
import torch
from pathlib import Path
from typing import List, Optional
import numpy as np

from ..core.config import settings
from ..core.logging import logger
from ..core.exceptions import ModelNotLoadedException, ImageProcessingException


class EmbeddingService:
    """Service for generating image embeddings using ImageBind model."""

    def __init__(self):
        self.model = None
        self.device = None
        self.is_loaded = False
        self._imagebind_module = None
        self._data_module = None
        self._modality_type = None

    def load_model(self) -> None:
        """Load the ImageBind model."""
        try:
            # Add ImageBind to path
            imagebind_path = Path(settings.IMAGEBIND_PATH)
            if imagebind_path.exists():
                sys.path.insert(0, str(imagebind_path))

            # Import ImageBind modules
            import imagebind
            from imagebind.models import imagebind_model
            from imagebind.models.imagebind_model import ModalityType
            from imagebind import data

            self._imagebind_module = imagebind
            self._data_module = data
            self._modality_type = ModalityType

            # Set device
            self.device = settings.DEVICE if torch.cuda.is_available() else "cpu"
            logger.info(f"Using device: {self.device}")

            # Load model
            logger.info("Loading ImageBind model...")
            self.model = imagebind_model.imagebind_huge(pretrained=True)
            self.model.eval()
            self.model.to(self.device)

            self.is_loaded = True
            logger.info("ImageBind model loaded successfully")

        except ImportError as e:
            logger.error(f"Failed to import ImageBind: {e}")
            logger.warning("Running in mock mode - embeddings will be random vectors")
            self._setup_mock_mode()
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise ModelNotLoadedException(f"Failed to load ImageBind model: {str(e)}")

    def _setup_mock_mode(self) -> None:
        """Setup mock mode for development without GPU."""
        self.device = "cpu"
        self.is_loaded = True
        self._mock_mode = True
        logger.warning("Running in MOCK MODE - using random embeddings")

    def _generate_mock_embedding(self) -> np.ndarray:
        """Generate a mock embedding for testing."""
        return np.random.randn(settings.EMBEDDING_DIM).astype(np.float32)

    def generate_embedding(self, image_path: str) -> List[float]:
        """
        Generate embedding for a single image.

        Args:
            image_path: Path to the image file

        Returns:
            List of floats representing the embedding
        """
        if not self.is_loaded:
            raise ModelNotLoadedException()

        try:
            # Mock mode for development
            if hasattr(self, '_mock_mode') and self._mock_mode:
                return self._generate_mock_embedding().tolist()

            # Load and transform image
            inputs = {
                self._modality_type.VISION: self._data_module.load_and_transform_vision_data(
                    [image_path], self.device
                )
            }

            # Generate embedding
            with torch.no_grad():
                embeddings = self.model(inputs)

            return embeddings[self._modality_type.VISION][0].cpu().numpy().tolist()

        except Exception as e:
            logger.error(f"Failed to generate embedding for {image_path}: {e}")
            raise ImageProcessingException(f"Failed to generate embedding: {str(e)}")

    def generate_embeddings_batch(self, image_paths: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple images.

        Args:
            image_paths: List of image file paths

        Returns:
            List of embeddings
        """
        if not self.is_loaded:
            raise ModelNotLoadedException()

        try:
            # Mock mode for development
            if hasattr(self, '_mock_mode') and self._mock_mode:
                return [self._generate_mock_embedding().tolist() for _ in image_paths]

            # Load and transform images
            inputs = {
                self._modality_type.VISION: self._data_module.load_and_transform_vision_data(
                    image_paths, self.device
                )
            }

            # Generate embeddings
            with torch.no_grad():
                embeddings = self.model(inputs)

            return embeddings[self._modality_type.VISION].cpu().numpy().tolist()

        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise ImageProcessingException(f"Failed to generate embeddings: {str(e)}")

    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        return {
            "loaded": self.is_loaded,
            "device": self.device,
            "embedding_dim": settings.EMBEDDING_DIM,
            "mock_mode": hasattr(self, '_mock_mode') and self._mock_mode
        }


# Singleton instance
embedding_service = EmbeddingService()

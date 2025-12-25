"""
Image processing service for handling image operations.
"""
import os
import uuid
import aiofiles
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image
import io

from ..core.config import settings
from ..core.logging import logger
from ..core.exceptions import ImageProcessingException, FileNotFoundException


class ImageProcessor:
    """Service for processing and managing images."""

    SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}

    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.data_dir = Path(settings.DATA_DIR)
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def is_valid_image(self, filename: str) -> bool:
        """Check if file has a valid image extension."""
        return Path(filename).suffix.lower() in self.SUPPORTED_EXTENSIONS

    async def save_upload(self, file_content: bytes, filename: str) -> str:
        """
        Save uploaded file to disk.

        Args:
            file_content: Raw file bytes
            filename: Original filename

        Returns:
            Path to saved file
        """
        try:
            # Generate unique filename
            ext = Path(filename).suffix.lower()
            unique_filename = f"{uuid.uuid4()}{ext}"
            filepath = self.upload_dir / unique_filename

            # Save file
            async with aiofiles.open(filepath, 'wb') as f:
                await f.write(file_content)

            logger.info(f"Saved uploaded file: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Failed to save upload: {e}")
            raise ImageProcessingException(f"Failed to save uploaded file: {str(e)}")

    def get_image_paths_for_category(self, category: str) -> List[str]:
        """
        Get all image paths for a given category.

        Args:
            category: Category name (e.g., 'Apparel_Boys')

        Returns:
            List of image file paths
        """
        category_dir = self.data_dir / category / "Images" / "images_with_product_ids"

        if not category_dir.exists():
            logger.warning(f"Category directory not found: {category_dir}")
            return []

        image_paths = []
        for root, _, files in os.walk(category_dir):
            for file in files:
                if self.is_valid_image(file):
                    image_paths.append(os.path.join(root, file))

        logger.info(f"Found {len(image_paths)} images in category: {category}")
        return image_paths

    def get_all_image_paths(self) -> dict[str, List[str]]:
        """
        Get all image paths organized by category.

        Returns:
            Dictionary mapping category names to lists of image paths
        """
        all_paths = {}
        for category in settings.PRODUCT_CATEGORIES:
            all_paths[category] = self.get_image_paths_for_category(category)
        return all_paths

    def validate_image(self, filepath: str) -> bool:
        """
        Validate that a file is a valid image.

        Args:
            filepath: Path to the image file

        Returns:
            True if valid image, False otherwise
        """
        try:
            with Image.open(filepath) as img:
                img.verify()
            return True
        except Exception:
            return False

    def get_image_info(self, filepath: str) -> dict:
        """
        Get information about an image.

        Args:
            filepath: Path to the image file

        Returns:
            Dictionary with image information
        """
        if not os.path.exists(filepath):
            raise FileNotFoundException(filepath)

        try:
            with Image.open(filepath) as img:
                return {
                    "path": filepath,
                    "format": img.format,
                    "mode": img.mode,
                    "size": img.size,
                    "width": img.width,
                    "height": img.height
                }
        except Exception as e:
            raise ImageProcessingException(f"Failed to get image info: {str(e)}")

    def resize_image(self, filepath: str, max_size: Tuple[int, int] = (800, 800)) -> bytes:
        """
        Resize image to fit within max dimensions.

        Args:
            filepath: Path to the image file
            max_size: Maximum (width, height)

        Returns:
            Resized image bytes
        """
        try:
            with Image.open(filepath) as img:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                buffer = io.BytesIO()
                img.save(buffer, format=img.format or 'JPEG')
                return buffer.getvalue()
        except Exception as e:
            raise ImageProcessingException(f"Failed to resize image: {str(e)}")

    def cleanup_upload(self, filepath: str) -> None:
        """Remove an uploaded file."""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Cleaned up upload: {filepath}")
        except Exception as e:
            logger.error(f"Failed to cleanup upload: {e}")

    def get_category_from_path(self, filepath: str) -> Optional[str]:
        """Extract category name from image path."""
        for category in settings.PRODUCT_CATEGORIES:
            if category in filepath:
                return category
        return None


# Singleton instance
image_processor = ImageProcessor()

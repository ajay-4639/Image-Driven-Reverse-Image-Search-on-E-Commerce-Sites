"""
Custom exception classes for the application.
"""
from fastapi import HTTPException, status


class ImageSearchException(Exception):
    """Base exception for image search operations."""
    def __init__(self, message: str = "An error occurred during image search"):
        self.message = message
        super().__init__(self.message)


class ModelNotLoadedException(ImageSearchException):
    """Raised when the ML model is not loaded."""
    def __init__(self, message: str = "Model not loaded. Please wait for initialization."):
        super().__init__(message)


class ImageProcessingException(ImageSearchException):
    """Raised when image processing fails."""
    def __init__(self, message: str = "Failed to process image"):
        super().__init__(message)


class CategoryNotFoundException(ImageSearchException):
    """Raised when a category is not found."""
    def __init__(self, category: str):
        super().__init__(f"Category '{category}' not found")
        self.category = category


class VectorDatabaseException(ImageSearchException):
    """Raised when vector database operations fail."""
    def __init__(self, message: str = "Vector database operation failed"):
        super().__init__(message)


class FileNotFoundException(ImageSearchException):
    """Raised when a file is not found."""
    def __init__(self, filepath: str):
        super().__init__(f"File not found: {filepath}")
        self.filepath = filepath


def raise_http_exception(exc: ImageSearchException, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
    """Convert custom exception to HTTP exception."""
    raise HTTPException(status_code=status_code, detail=exc.message)

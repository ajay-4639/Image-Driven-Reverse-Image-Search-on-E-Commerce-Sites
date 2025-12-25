# Backend - Image Search API

FastAPI backend for the Image-Driven Reverse Image Search application.

## Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py      # Health check endpoints
│   │   │   ├── search.py      # Image search endpoints
│   │   │   ├── categories.py  # Category endpoints
│   │   │   └── images.py      # Image serving endpoints
│   │   └── router.py          # API router aggregator
│   ├── core/
│   │   ├── config.py          # Application settings
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── logging.py         # Logging configuration
│   ├── models/
│   │   └── schemas.py         # Pydantic schemas
│   ├── services/
│   │   ├── embedding_service.py   # ImageBind embeddings
│   │   ├── image_processor.py     # Image handling
│   │   ├── search_service.py      # Search orchestration
│   │   └── vector_store.py        # Qdrant operations
│   └── main.py                # Application entry point
├── Dockerfile                 # CPU Docker image
├── Dockerfile.gpu             # GPU Docker image
├── requirements.txt           # Python dependencies
└── .env.example              # Environment template
```

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup ImageBind (in parent directory)
git clone https://github.com/facebookresearch/ImageBind.git ../ImageBind
cd ../ImageBind && pip install -e . && cd ../backend

# Configure environment
cp .env.example .env

# Run the server
uvicorn app.main:app --reload --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Environment Variables

See `.env.example` for all available configuration options.

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

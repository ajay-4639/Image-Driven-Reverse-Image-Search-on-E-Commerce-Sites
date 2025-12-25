# Image-Driven Reverse Image Search for E-Commerce

A full-stack application for performing reverse image search on e-commerce products using Meta's ImageBind model and Qdrant vector database.

## Features

- **Reverse Image Search**: Upload an image to find visually similar products
- **Category Browsing**: Browse products by category (Apparel Boys, Apparel Girls, Footwear Men, Footwear Women)
- **Modern React Frontend**: Clean, responsive UI with Tailwind CSS
- **FastAPI Backend**: RESTful API with automatic documentation
- **Docker Support**: Easy deployment with Docker Compose
- **GPU Acceleration**: Optional CUDA support for faster processing

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React         │────▶│   FastAPI       │────▶│   Qdrant        │
│   Frontend      │     │   Backend       │     │   Vector DB     │
│   (Vite + TS)   │     │   (Python)      │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                        ┌────────▼────────┐
                        │   ImageBind     │
                        │   (Meta AI)     │
                        └─────────────────┘
```

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   └── routes/     # Route handlers
│   │   ├── core/           # Configuration, logging, exceptions
│   │   ├── models/         # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── Dockerfile
│   ├── Dockerfile.gpu
│   └── requirements.txt
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utility functions
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml      # Production compose
├── docker-compose.dev.yml  # Development compose
├── docker-compose.gpu.yml  # GPU-enabled compose
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)
- NVIDIA GPU + CUDA (optional, for GPU acceleration)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Image-Driven-Reverse-Image-Search-on-E-Commerce-Sites.git
   cd Image-Driven-Reverse-Image-Search-on-E-Commerce-Sites
   ```

2. **Setup the dataset**

   Download the Fashion Images dataset from Kaggle and place it in the `data/` directory:
   ```
   data/
   └── fashion-images/
       ├── Apparel_Boys/
       ├── Apparel_Girls/
       ├── Footwear_Men/
       └── Footwear_Women/
   ```

3. **Setup ImageBind**
   ```bash
   git clone https://github.com/facebookresearch/ImageBind.git
   cd ImageBind
   pip install -e .
   ```

4. **Start the application**
   ```bash
   # Production mode
   docker-compose up -d

   # Development mode (with hot reload)
   docker-compose -f docker-compose.dev.yml up

   # With GPU support
   docker-compose -f docker-compose.gpu.yml up -d
   ```

5. **Access the application**
   - Frontend: http://localhost:80 (or http://localhost:3000 in dev)
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the server
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Run development server
npm run dev
```

## API Endpoints

### Health Check
- `GET /api/v1/health` - Service health status
- `GET /api/v1/health/ready` - Readiness check
- `GET /api/v1/health/live` - Liveness check
- `GET /api/v1/health/indexing` - Indexing status

### Search
- `POST /api/v1/search` - Search by uploaded image
- `POST /api/v1/search/url` - Search by image URL (not yet implemented)

### Categories
- `GET /api/v1/categories` - List all categories
- `GET /api/v1/categories/{category}` - Get category images
- `GET /api/v1/categories/{category}/random` - Get random images from category

### Images
- `GET /api/v1/images/file` - Serve image file
- `GET /api/v1/images/info` - Get image metadata

## Configuration

### Backend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | Image Search API | Application name |
| `DEBUG` | false | Enable debug mode |
| `DEVICE` | cuda | Device for ML model (cuda/cpu) |
| `DATA_DIR` | ./data/fashion-images | Path to image data |
| `UPLOAD_DIR` | ./uploads | Path for uploaded images |
| `IMAGEBIND_PATH` | ./ImageBind | Path to ImageBind installation |
| `USE_IN_MEMORY` | true | Use in-memory Qdrant |
| `QDRANT_HOST` | localhost | Qdrant host |
| `QDRANT_PORT` | 6333 | Qdrant port |
| `CORS_ORIGINS` | ["http://localhost:3000"] | Allowed CORS origins |

### Frontend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | /api/v1 | Backend API URL |

## Technologies

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **ImageBind** - Meta's multimodal AI model
- **Qdrant** - Vector similarity search engine
- **PyTorch** - Deep learning framework
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **Lucide React** - Icons

### Infrastructure
- **Docker** - Containerization
- **Nginx** - Reverse proxy
- **Docker Compose** - Orchestration

## Screenshots

### Home Page
The landing page with feature overview and quick access to search and categories.

### Search Page
Upload an image to find similar products from the catalog.

### Categories Page
Browse products organized by category.

## Original Implementation

This project was originally built with Gradio. The original implementation is preserved in [app.py](app.py).

**Original Tab 0:** ![](assets/Tab0.jpg)
**Original Tab 1:** ![](assets/Tab1.jpg)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Meta ImageBind](https://github.com/facebookresearch/ImageBind) - Multimodal AI model
- [Qdrant](https://qdrant.tech/) - Vector search engine
- [Fashion Images Dataset](https://www.kaggle.com/) - Product images from Kaggle

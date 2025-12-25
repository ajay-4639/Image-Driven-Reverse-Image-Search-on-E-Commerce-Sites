# Makefile for Image Search Application

.PHONY: help install dev build start stop clean logs

# Default target
help:
	@echo "Image Search Application - Available Commands:"
	@echo ""
	@echo "  make install    - Install all dependencies"
	@echo "  make dev        - Start development servers"
	@echo "  make build      - Build Docker images"
	@echo "  make start      - Start production containers"
	@echo "  make stop       - Stop all containers"
	@echo "  make clean      - Remove containers and volumes"
	@echo "  make logs       - View container logs"
	@echo ""
	@echo "Development:"
	@echo "  make backend    - Start backend dev server"
	@echo "  make frontend   - Start frontend dev server"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-dev - Start with docker-compose.dev.yml"
	@echo "  make docker-gpu - Start with GPU support"

# Install dependencies
install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

# Development
dev:
	@echo "Starting development servers..."
	@make -j2 backend frontend

backend:
	cd backend && uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

# Docker commands
build:
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down

clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

logs:
	docker-compose logs -f

# Docker development
docker-dev:
	docker-compose -f docker-compose.dev.yml up

docker-gpu:
	docker-compose -f docker-compose.gpu.yml up -d

# Utility
lint:
	cd backend && python -m flake8 app/
	cd frontend && npm run lint

format:
	cd backend && python -m black app/
	cd frontend && npm run format

test:
	cd backend && python -m pytest
	cd frontend && npm run test

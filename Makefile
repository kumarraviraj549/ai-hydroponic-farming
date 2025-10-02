.PHONY: help install dev build test clean docker-up docker-down init-db seed-db lint
.DEFAULT_GOAL := help

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)HydroAI Development Commands$(NC)"
	@echo "$(BLUE)==============================$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

# Installation
install: ## Install all dependencies (backend and frontend)
	@echo "$(GREEN)Installing all dependencies...$(NC)"
	npm install
	cd frontend && npm install
	cd backend && pip install -r requirements.txt
	@echo "$(GREEN)✅ All dependencies installed successfully!$(NC)"

install-backend: ## Install backend dependencies only
	@echo "$(GREEN)Installing backend dependencies...$(NC)"
	cd backend && pip install -r requirements.txt
	@echo "$(GREEN)✅ Backend dependencies installed!$(NC)"

install-frontend: ## Install frontend dependencies only
	@echo "$(GREEN)Installing frontend dependencies...$(NC)"
	npm install
	cd frontend && npm install
	@echo "$(GREEN)✅ Frontend dependencies installed!$(NC)"

# Development
dev: ## Start both backend and frontend in development mode
	@echo "$(GREEN)Starting development servers...$(NC)"
	npm run dev

dev-backend: ## Start backend development server only
	@echo "$(GREEN)Starting backend development server...$(NC)"
	cd backend && python app.py

dev-frontend: ## Start frontend development server only
	@echo "$(GREEN)Starting frontend development server...$(NC)"
	cd frontend && npm run dev

# Database
init-db: ## Initialize database with tables
	@echo "$(GREEN)Initializing database...$(NC)"
	cd backend && python init_db.py
	@echo "$(GREEN)✅ Database initialized!$(NC)"

reset-db: ## Reset database (drop and recreate all tables)
	@echo "$(YELLOW)Resetting database (this will delete all data)...$(NC)"
	cd backend && python init_db.py --drop
	@echo "$(GREEN)✅ Database reset complete!$(NC)"

seed-db: ## Seed database with demo data
	@echo "$(GREEN)Seeding database with demo data...$(NC)"
	cd backend && python seed_demo_data.py
	@echo "$(GREEN)✅ Demo data seeded!$(NC)"

check-db: ## Check database connection
	@echo "$(GREEN)Checking database connection...$(NC)"
	cd backend && python init_db.py --check-connection

# Build
build: ## Build frontend for production
	@echo "$(GREEN)Building frontend...$(NC)"
	cd frontend && npm run build
	@echo "$(GREEN)✅ Frontend built successfully!$(NC)"

build-frontend: build ## Alias for build

# Testing
test: ## Run all tests
	@echo "$(GREEN)Running tests...$(NC)"
	$(MAKE) test-backend
	$(MAKE) lint-frontend

test-backend: ## Run backend tests
	@echo "$(GREEN)Running backend tests...$(NC)"
	cd backend && python -m pytest -v

test-frontend: ## Run frontend tests
	@echo "$(GREEN)Running frontend tests...$(NC)"
	cd frontend && npm test

# Linting
lint: ## Run all linting
	@echo "$(GREEN)Running linting...$(NC)"
	$(MAKE) lint-backend
	$(MAKE) lint-frontend

lint-backend: ## Run backend linting
	@echo "$(GREEN)Running backend linting...$(NC)"
	cd backend && python -m flake8 .
	cd backend && python -m black . --check

lint-frontend: ## Run frontend linting
	@echo "$(GREEN)Running frontend linting...$(NC)"
	cd frontend && npm run lint

fix-lint: ## Fix linting issues
	@echo "$(GREEN)Fixing linting issues...$(NC)"
	cd backend && python -m black .
	cd frontend && npm run lint --fix

# Docker
docker-build: ## Build Docker images
	@echo "$(GREEN)Building Docker images...$(NC)"
	docker-compose build
	@echo "$(GREEN)✅ Docker images built!$(NC)"

docker-up: ## Start services with Docker Compose
	@echo "$(GREEN)Starting Docker services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Services started! Check http://localhost:3000$(NC)"

docker-down: ## Stop Docker services
	@echo "$(YELLOW)Stopping Docker services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Services stopped!$(NC)"

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-logs-backend: ## View backend Docker logs
	docker-compose logs -f backend

docker-logs-frontend: ## View frontend Docker logs
	docker-compose logs -f frontend

# Cleanup
clean: ## Clean all build artifacts and dependencies
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
	rm -rf node_modules
	rm -rf frontend/node_modules
	rm -rf frontend/.next
	rm -rf backend/__pycache__
	rm -rf backend/**/__pycache__
	rm -rf backend/*.pyc
	rm -rf backend/logs/*.log
	@echo "$(GREEN)✅ Cleanup complete!$(NC)"

clean-docker: ## Clean Docker resources
	@echo "$(YELLOW)Cleaning Docker resources...$(NC)"
	docker-compose down -v --remove-orphans
	docker system prune -f
	@echo "$(GREEN)✅ Docker cleanup complete!$(NC)"

# Production
start: ## Start production servers
	@echo "$(GREEN)Starting production servers...$(NC)"
	npm run start

start-backend: ## Start backend production server
	@echo "$(GREEN)Starting backend production server...$(NC)"
	cd backend && gunicorn -w 4 -b 0.0.0.0:5000 app:app

start-frontend: ## Start frontend production server
	@echo "$(GREEN)Starting frontend production server...$(NC)"
	cd frontend && npm run start

# Utilities
backup-db: ## Backup database (SQLite only)
	@echo "$(GREEN)Backing up database...$(NC)"
	cp backend/hydroai.db backend/hydroai.db.backup.$(shell date +%Y%m%d_%H%M%S)
	@echo "$(GREEN)✅ Database backed up!$(NC)"

restore-db: ## Restore database from backup (provide BACKUP_FILE=filename)
	test -n "$(BACKUP_FILE)" || (echo "$(RED)Please provide BACKUP_FILE=filename$(NC)" && exit 1)
	@echo "$(GREEN)Restoring database from $(BACKUP_FILE)...$(NC)"
	cp "$(BACKUP_FILE)" backend/hydroai.db
	@echo "$(GREEN)✅ Database restored!$(NC)"

status: ## Show development environment status
	@echo "$(BLUE)HydroAI Development Environment Status$(NC)"
	@echo "$(BLUE)======================================$(NC)"
	@echo "Frontend: $(shell cd frontend && npm list next 2>/dev/null | grep next || echo 'Not installed')"
	@echo "Backend: $(shell cd backend && python --version 2>/dev/null || echo 'Python not found')"
	@echo "Database: $(shell test -f backend/hydroai.db && echo 'SQLite database exists' || echo 'Database not initialized')"
	@echo "Docker: $(shell docker --version 2>/dev/null || echo 'Docker not installed')"

# Quick setup for new developers
setup: ## Complete setup for new developers
	@echo "$(BLUE)🚀 Setting up HydroAI for development...$(NC)"
	$(MAKE) install
	$(MAKE) init-db
	$(MAKE) seed-db
	@echo "$(GREEN)✅ Setup complete! Run 'make dev' to start development.$(NC)"

setup-docker: ## Complete Docker setup
	@echo "$(BLUE)🐳 Setting up HydroAI with Docker...$(NC)"
	$(MAKE) docker-build
	$(MAKE) docker-up
	@echo "$(GREEN)✅ Docker setup complete! App available at http://localhost:3000$(NC)"

# Info
info: ## Show project information
	@echo "$(BLUE)HydroAI - AI-Powered Hydroponic Farming SaaS Platform$(NC)"
	@echo "$(BLUE)======================================================$(NC)"
	@echo "Frontend: Next.js + TypeScript + Tailwind CSS"
	@echo "Backend: Flask + SQLAlchemy + JWT"
	@echo "Database: PostgreSQL / SQLite"
	@echo "WebSocket: Real-time sensor data"
	@echo ""
	@echo "Demo Credentials:"
	@echo "Email: demo@hydroai.com"
	@echo "Password: demo123"
	@echo ""
	@echo "Endpoints:"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:5000"
	@echo "Health Check: http://localhost:5000/api/v1/health"
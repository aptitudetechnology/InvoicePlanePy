.PHONY: help build up down logs shell db-init db-shell test test-routes test-sqlalchemy clean

# Default target
help:
	@echo "InvoicePlane Python - Development Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make build         - Build Docker containers"
	@echo "  make up            - Start the application"
	@echo "  make down          - Stop the application"
	@echo "  make logs          - View application logs"
	@echo "  make shell         - Open shell in web container"
	@echo "  make db-init       - Initialize database with seed data"
	@echo "  make setup         - Run complete database setup (like PHP installer)"
	@echo "  make create-admin  - Create admin user"
	@echo "  make db-shell      - Open PostgreSQL shell"
	@echo "  make test          - Run tests"
	@echo "  make test-routes   - Test API routes and authentication"
	@echo "  make test-sqlalchemy - Test SQLAlchemy models for issues"
	@echo "  make clean         - Clean up containers and volumes"
	@echo ""

# Build containers
build:
	docker-compose -f docker-compose.python.yml build

# Start application
up:
	docker-compose -f docker-compose.python.yml up -d
	@echo ""
	@echo "🚀 InvoicePlane Python is starting..."
	@echo "📱 Web interface: http://localhost:8080"
	@echo "🗄️  Database: localhost:5432"
	@echo ""
	@echo "⏳ The application will automatically:"
	@echo "   • Initialize the database"
	@echo "   • Create tables"
	@echo "   • Create admin user"
	@echo ""
	@echo "Demo credentials:"
	@echo "  Admin: admin / admin123"
	@echo "  User:  user / user123"
	@echo ""
	@echo "Run 'make logs' to see startup progress"

# Start with logs
up-logs:
	docker-compose -f docker-compose.python.yml up

# Stop application
down:
	docker-compose -f docker-compose.python.yml down

# View logs
logs:
	docker-compose -f docker-compose.python.yml logs -f web

# Open shell in web container
shell:
	docker-compose -f docker-compose.python.yml exec web bash

# Initialize database with seed data
db-init:
	docker-compose -f docker-compose.python.yml exec web python init_db.py

# Run complete database setup (like PHP InvoicePlane installer)
setup:
	docker-compose -f docker-compose.python.yml exec web python setup/setup_manager.py

# Create admin user
create-admin:
	docker-compose -f docker-compose.python.yml exec web python scripts/create_admin_user.py

# Open PostgreSQL shell
db-shell:
	docker-compose -f docker-compose.python.yml exec db psql -U invoiceplane -d invoiceplane

# Test database models
test-models:
	docker-compose -f docker-compose.python.yml exec web python test_models.py

# Test SQLAlchemy models with detailed analysis
test-sqlalchemy:
	@echo "🔍 Testing SQLAlchemy models for relationship issues..."
	python scripts/test-SQLAlchemy-models.py

# Test API routes and authentication
test-routes:
	@echo "🔍 Testing FastAPI routes..."
	python scripts/test_routes.py

# Run tests
test:
	docker-compose -f docker-compose.python.yml exec web python -m pytest tests/ -v

# Development setup (build, start, and initialize)
dev-setup: build up
	@echo "⏳ Waiting for containers to start and database to initialize..."
	@sleep 15
	@echo "📊 Checking application status..."
	@make status
	@echo ""
	@echo "✅ Development environment ready!"
	@echo "🌐 Open http://localhost:8080 in your browser"
	@echo "🔑 Admin credentials: admin / admin123"

# Clean up everything
clean:
	docker-compose -f docker-compose.python.yml down -v
	docker system prune -f

# Restart application
restart: down up

# View database logs
db-logs:
	docker-compose -f docker-compose.python.yml logs -f db

# Backup database
db-backup:
	docker-compose -f docker-compose.python.yml exec db pg_dump -U invoiceplane invoiceplane > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Show running containers
status:
	docker-compose -f docker-compose.python.yml ps

# Install Python dependencies locally (for IDE support)
install-local:
	pip install -r requirements.txt

# Format code
format:
	docker-compose -f docker-compose.python.yml exec web black app/ --line-length 88
	docker-compose -f docker-compose.python.yml exec web isort app/

# Lint code
lint:
	docker-compose -f docker-compose.python.yml exec web flake8 app/
	docker-compose -f docker-compose.python.yml exec web mypy app/

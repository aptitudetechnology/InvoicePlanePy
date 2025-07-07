# InvoicePlane Python - Phase 1 MVP

A modern Python rewrite of InvoicePlane using FastAPI, SQLAlchemy, and PostgreSQL.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Make (optional, for convenience commands)

### Option 1: Using Make (Recommended)
```bash
# Start everything with one command
make dev-setup

# View the application
open http://localhost:8080
```

### Option 2: Manual Docker Commands
```bash
# Build and start containers
docker-compose -f docker-compose.python.yml up --build -d

# Initialize database with seed data
docker-compose -f docker-compose.python.yml exec web python init_db.py

# View logs
docker-compose -f docker-compose.python.yml logs -f web
```

### Option 3: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Start PostgreSQL (you'll need to adjust DATABASE_URL in .env)
# Then run the app
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📱 Access the Application

- **Web Interface**: http://localhost:8080
- **Database**: localhost:5432
- **API Docs**: http://localhost:8080/docs (FastAPI automatic documentation)

## 🔐 Demo Credentials

- **Admin**: username: `admin`, password: `admin123`
- **User**: username: `user`, password: `user123`

## 📋 Available Make Commands

```bash
make help          # Show all available commands
make up            # Start the application
make down          # Stop the application
make logs          # View application logs
make shell         # Open shell in web container
make db-init       # Initialize database with seed data
make db-shell      # Open PostgreSQL shell
make test-routes   # Test API routes and authentication
make test-models   # Test database models
make restart       # Restart the application
make clean         # Clean up containers and volumes
```

## 🏗️ Phase 1 Features Completed

### ✅ Core Infrastructure
- [x] FastAPI application setup
- [x] PostgreSQL database with SQLAlchemy
- [x] Docker containerization
- [ ] User authentication with JWT
- [x] Basic routing structure

### ✅ Dashboard
- [x] Working dashboard with statistics
- [x] Invoice overview cards
- [x] Recent invoices list
- [ ] Financial summary

### ✅ Navigation & UI
- [x] Bootstrap-based responsive UI
- [x] Sidebar navigation
- [x] User authentication pages
- [x] Dashboard layout

### ✅ Basic Models
- [x] User model with authentication
- [x] Client model
- [x] Invoice and InvoiceItem models
- [x] Database relationships

### ✅ Basic Views
- [x] Login/logout functionality
- [x] Dashboard with real data
- [x] Client list page
- [x] Invoice list page
- [x] Create forms (UI only)

### ✅ Development Tools
- [x] Makefile for easy commands
- [x] Database seeding script
- [x] Environment configuration
- [x] Docker development setup
- [x] Route testing script for debugging
- [x] Authentication debugging tools

## 🔄 Next: Phase 2 (Weeks 3-4)

The next phase will focus on making the forms functional:

- [ ] Client CRUD operations
- [ ] Invoice creation and editing
- [ ] Product management
- [ ] Basic PDF generation
- [ ] Email sending functionality

## 🐛 Troubleshooting

### Authentication Issues
```bash
# Test authentication routes
make test-routes

# Check route registration in app logs
make logs | grep "FastAPI Routes"

# Debug routes endpoint
curl http://localhost:8080/debug/routes
```

### Database Connection Issues
```bash
# Check if containers are running
make status

# View database logs
make db-logs

# Restart everything
make restart
```

### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### Port Conflicts
If port 8080 or 5432 are already in use, edit `docker-compose.python.yml` to use different ports.

## 📁 Project Structure

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration settings
├── database.py          # Database connection setup
├── dependencies.py      # FastAPI dependencies
├── models/              # SQLAlchemy models
├── routers/             # API route handlers
├── core/                # Core utilities (security, etc.)
└── templates/           # Jinja2 HTML templates

scripts/                 # Development and testing scripts
├── test_routes.py       # Route testing and debugging
static/                  # Static files (CSS, JS, images)
tests/                   # Test suite (future)
migrations/              # Database migrations (future)
```

## 🔧 Development Features

### Route Debugging
The application includes built-in debugging features:

- **Route Registration**: Check startup logs to see all registered routes
- **Debug Endpoint**: Visit `/debug/routes` to see all routes in JSON format
- **Test Script**: Use `make test-routes` to test authentication and API endpoints

### Authentication System
- Session-based authentication with JWT tokens
- Cookie-based session management
- User roles and permissions (admin/user)
- Secure password hashing with bcrypt

### Quick Debugging Commands
```bash
# Test if app is running and routes are working
make test-routes

# Check what routes are registered
curl http://localhost:8080/debug/routes | jq

# See route registration in startup logs
make logs | grep -A 20 "FastAPI Routes Registered"

# Test login directly
curl -X POST http://localhost:8080/auth/login \
  -d "username=admin&password=admin123" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -v
```

This completes Phase 1 of the InvoicePlane Python migration! 🎉

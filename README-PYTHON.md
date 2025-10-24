# InvoicePlane Python - Phase 1 MVP

This is Phase 1 of the InvoicePlane PHP to Python migration, featuring a working dashboard with navigation and basic invoice/client management.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Setup

1. **Clone and start the application:**
   ```bash
   # Start the application with Docker
   docker-compose -f docker-compose.python.yml up --build
   ```

2. **Initialize the database (in another terminal):**
   ```bash
   # Initialize database and create seed data
   docker-compose -f docker-compose.python.yml exec web python init_db.py
   ```

3. **Access the application:**
   - Open your browser to: http://localhost:8000
   - Login with demo credentials:
     - **Admin**: `admin` / `admin123`
     - **User**: `user` / `user123`

## 📋 Phase 1 Features

### ✅ Completed
- **🐳 Docker Environment**: Complete containerized setup with PostgreSQL
- **🔐 Authentication System**: JWT-based login with session management
- **📊 Dashboard**: Overview with invoice statistics and recent invoices
- **👥 Client Management**: List and create clients (basic forms)
- **📄 Invoice Management**: List and create invoices (basic forms)
- **🎨 Modern UI**: Bootstrap 5 responsive interface
- **🗄️ Database Models**: SQLAlchemy models for core entities
- **🌱 Seed Data**: Demo data for testing

### 🎯 Current Functionality
1. **Dashboard**
   - Invoice statistics (total, paid, draft, overdue)
   - Financial overview (revenue, outstanding amounts)
   - Client overview (total, active)
   - Recent invoices list

2. **Client Management**
   - View all clients
   - Client creation form (not yet functional)
   - Client status tracking

3. **Invoice Management**
   - View all invoices with status
   - Invoice creation form (not yet functional)
   - Status indicators

4. **Navigation**
   - Responsive sidebar navigation
   - User dropdown with logout
   - Breadcrumb navigation

## 🏗️ Architecture

```
app/
├── models/          # SQLAlchemy database models
├── routers/         # FastAPI route handlers
├── templates/       # Jinja2 HTML templates
├── core/           # Security and utilities
├── config.py       # Application configuration
├── database.py     # Database connection
└── main.py         # FastAPI application
```

## 🗄️ Database Schema

### Core Models
- **User**: Authentication and user management
- **Client**: Customer information and contacts
- **Invoice**: Invoice headers with status tracking
- **InvoiceItem**: Line items for invoices

### Sample Data
The seed script creates:
- 2 demo users (admin/user)
- 3 sample clients
- 3 sample invoices in different states

## 🔧 Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the application
python -m app.main
```

### Database Management
```bash
# Initialize database
python init_db.py

# Connect to database
docker-compose -f docker-compose.python.yml exec db psql -U invoiceplane -d invoiceplane
```

## 📝 API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Process login
- `POST /logout` - Logout

### Dashboard
- `GET /` - Redirect to dashboard
- `GET /dashboard` - Main dashboard

### Clients
- `GET /clients` - Client list
- `GET /clients/create` - Client creation form

### Invoices
- `GET /invoices` - Invoice list
- `GET /invoices/create` - Invoice creation form

## 🔄 Next Steps (Phase 2)

1. **Functional Forms**: Make client and invoice creation work
2. **CRUD Operations**: Complete edit/delete functionality
3. **Invoice Items**: Dynamic line item management
4. **PDF Generation**: Invoice PDF export
5. **Email Integration**: Send invoices via email
6. **Advanced Features**: Search, filtering, pagination

## 🐛 Known Issues

1. **Forms Not Functional**: Create/edit forms are UI-only (Phase 2)
2. **No PDF Generation**: PDF functionality planned for Phase 2
3. **No Email**: Email sending planned for Phase 2
4. **Limited Validation**: Basic validation only

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop and mobile
- **Modern Bootstrap 5**: Clean, professional interface
- **Status Indicators**: Color-coded invoice statuses
- **Interactive Navigation**: Active page highlighting
- **Loading States**: Proper form feedback

## 📊 Phase 1 Success Criteria ✅

- [x] Working Docker environment
- [x] User authentication with JWT
- [x] Dashboard with real data display
- [x] Navigation between sections
- [x] Basic client and invoice listing
- [x] Professional UI with Bootstrap 5
- [x] Database models and relationships
- [x] Seed data for demonstration

## 🚧 Technical Debt

1. **Error Handling**: Basic error handling implemented
2. **Input Validation**: Server-side validation needed
3. **Security**: CSRF protection needed for production
4. **Logging**: Application logging to be added
5. **Testing**: Unit tests to be written

---

**Migration Progress**: Phase 1 Complete ✅ | Next: Phase 2 - Functional CRUD Operations

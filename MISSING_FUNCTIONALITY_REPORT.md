# InvoicePlane PHP to Python Migration Plan

## Overview
This document outlines a comprehensive migration strategy for converting InvoicePlane from PHP/CodeIgniter 3.13 to Python. The migration will maintain all existing functionality while modernizing the architecture and improving maintainability.

## Current Architecture Analysis

### Database Schema
Based on analysis of the SQL schema files, the core entities are:
- **Clients**: Customer/client management
- **Invoices**: Main invoice functionality with status tracking
- **Invoice Items**: Line items for invoices
- **Products**: Product catalog
- **Projects & Tasks**: Project management functionality
- **Payments**: Payment tracking
- **Users**: User authentication and management
- **Custom Fields**: Extensible field system

### Core Modules Identified
```
application/modules/
├── clients/          # Client management
├── invoices/         # Invoice creation, editing, status management
├── quotes/           # Quote functionality
├── products/         # Product catalog
├── projects/         # Project management
├── tasks/            # Task tracking
├── payments/         # Payment processing
├── reports/          # Reporting system
├── users/            # User management
├── settings/         # Application configuration
├── email_templates/  # Email template management
├── custom_fields/    # Custom field definitions
└── dashboard/        # Main dashboard
```

## Target Python Architecture

### Framework Choice: FastAPI
**Rationale**: FastAPI provides:
- Automatic API documentation
- Built-in data validation with Pydantic
- High performance (comparable to Node.js/Go)
- Modern Python features (async/await, type hints)
- Easy deployment and containerization

### Project Structure
```
invoiceplane_py/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Application configuration
│   ├── database.py                # Database connection and session management
│   ├── dependencies.py            # FastAPI dependencies (auth, db sessions)
│   │
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py                # Base model class
│   │   ├── client.py              # Client model
│   │   ├── invoice.py             # Invoice and related models
│   │   ├── product.py             # Product model
│   │   ├── project.py             # Project and task models
│   │   ├── payment.py             # Payment model
│   │   ├── user.py                # User and authentication models
│   │   └── custom_field.py        # Custom fields model
│   │
│   ├── schemas/                   # Pydantic schemas for API validation
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── invoice.py
│   │   ├── product.py
│   │   ├── project.py
│   │   ├── payment.py
│   │   ├── user.py
│   │   └── common.py              # Common schema types
│   │
│   ├── routers/                   # API route handlers (equivalent to controllers)
│   │   ├── __init__.py
│   │   ├── auth.py                # Authentication routes
│   │   ├── clients.py             # Client management routes
│   │   ├── invoices.py            # Invoice management routes
│   │   ├── products.py            # Product management routes
│   │   ├── projects.py            # Project management routes
│   │   ├── payments.py            # Payment routes
│   │   ├── reports.py             # Reporting routes
│   │   ├── dashboard.py           # Dashboard routes
│   │   └── settings.py            # Settings routes
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── client_service.py
│   │   ├── invoice_service.py
│   │   ├── product_service.py
│   │   ├── project_service.py
│   │   ├── payment_service.py
│   │   ├── email_service.py
│   │   ├── pdf_service.py
│   │   └── auth_service.py
│   │
│   ├── core/                      # Core utilities and helpers
│   │   ├── __init__.py
│   │   ├── security.py            # Password hashing, JWT handling
│   │   ├── exceptions.py          # Custom exception classes
│   │   ├── utils.py               # Utility functions
│   │   ├── validators.py          # Custom validation functions
│   │   └── pagination.py          # Pagination helpers
│   │
│   └── templates/                 # Jinja2 templates (if serving HTML)
│       ├── base.html
│       ├── dashboard/
│       ├── clients/
│       ├── invoices/
│       └── auth/
│
├── migrations/                    # Alembic database migrations
│   ├── versions/
│   ├── alembic.ini
│   └── env.py
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── conftest.py                # Test configuration
│   ├── test_models/
│   ├── test_routers/
│   └── test_services/
│
├── static/                        # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # Docker configuration
├── Dockerfile                     # Docker build file
├── .env.example                   # Environment variables template
└── README.md                      # Project documentation
```

## Database Models Migration

### 1. Base Model Pattern
```python
# app/models/base.py
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import Dict, Any

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def get_by_id(cls, db: Session, id: int):
        """Get record by ID"""
        return db.query(cls).filter(cls.id == id).first()
```

### 2. Client Model Migration
```python
# app/models/client.py
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel

class Client(BaseModel):
    __tablename__ = "clients"
    
    # Core fields (mapping from ip_clients table)
    name = Column(String(100), nullable=False)  # client_name
    surname = Column(String(100))               # client_surname  
    title = Column(String(50))                  # client_title
    company = Column(String(255))               # client_company
    
    # Contact information
    email = Column(String(100))                 # client_email
    phone = Column(String(20))                  # client_phone
    mobile = Column(String(20))                 # client_mobile
    fax = Column(String(20))                    # client_fax
    website = Column(String(100))               # client_web
    
    # Address fields
    address_1 = Column(String(100))             # client_address_1
    address_2 = Column(String(100))             # client_address_2
    city = Column(String(45))                   # client_city
    state = Column(String(35))                  # client_state
    zip_code = Column(String(15))               # client_zip
    country = Column(String(35))                # client_country
    
    # Business details
    vat_id = Column(String(50))                 # client_vat_id
    tax_code = Column(String(50))               # client_tax_code
    
    # Status and settings
    is_active = Column(Boolean, default=True)   # client_active
    language = Column(String(10))               # client_language
    
    # Relationships
    invoices = relationship("Invoice", back_populates="client")
    quotes = relationship("Quote", back_populates="client")
    projects = relationship("Project", back_populates="client")
    notes = relationship("ClientNote", back_populates="client")
    
    @property
    def full_name(self) -> str:
        """Get client's full name"""
        if self.surname:
            return f"{self.name} {self.surname}"
        return self.name
    
    @property
    def display_name(self) -> str:
        """Get display name (company or full name)"""
        return self.company if self.company else self.full_name
```

### 3. Invoice Model Migration
```python
# app/models/invoice.py
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Decimal, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel

class InvoiceStatus(PyEnum):
    DRAFT = 1
    SENT = 2
    VIEWED = 3
    PAID = 4
    OVERDUE = 5
    CANCELLED = 6

class Invoice(BaseModel):
    __tablename__ = "invoices"
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    invoice_group_id = Column(Integer, ForeignKey("invoice_groups.id"))
    
    # Invoice details
    invoice_number = Column(String(20), unique=True, nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    
    # Dates
    issue_date = Column(Date, nullable=False)    # invoice_date_created
    due_date = Column(Date, nullable=False)      # invoice_date_due
    
    # Content
    terms = Column(Text)                         # invoice_terms
    notes = Column(Text)
    
    # Security
    url_key = Column(String(32), unique=True)    # invoice_url_key
    
    # Calculated fields (from ip_invoice_amounts)
    subtotal = Column(Decimal(10, 2), default=0)
    tax_total = Column(Decimal(10, 2), default=0)
    total = Column(Decimal(10, 2), default=0)
    paid_amount = Column(Decimal(10, 2), default=0)
    balance = Column(Decimal(10, 2), default=0)
    
    # Relationships
    client = relationship("Client", back_populates="invoices")
    user = relationship("User", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="invoice")
    recurring_settings = relationship("InvoiceRecurring", back_populates="invoice", uselist=False)
    
    @property
    def is_overdue(self) -> bool:
        """Check if invoice is overdue"""
        from datetime import date
        return (self.status not in [InvoiceStatus.DRAFT, InvoiceStatus.PAID] 
                and self.due_date < date.today())
    
    @property
    def days_overdue(self) -> int:
        """Calculate days overdue"""
        if not self.is_overdue:
            return 0
        from datetime import date
        return (date.today() - self.due_date).days

class InvoiceItem(BaseModel):
    __tablename__ = "invoice_items"
    
    # Foreign keys
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    tax_rate_id = Column(Integer, ForeignKey("tax_rates.id"))
    
    # Item details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    quantity = Column(Decimal(10, 2), nullable=False)
    price = Column(Decimal(10, 2), nullable=False)
    order = Column(Integer, default=0)
    
    # Calculated amounts
    subtotal = Column(Decimal(10, 2))
    tax_amount = Column(Decimal(10, 2))
    total = Column(Decimal(10, 2))
    
    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")
    tax_rate = relationship("TaxRate")
```

### 4. Product Model Migration
```python
# app/models/product.py
from sqlalchemy import Column, Integer, String, Text, Decimal, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"
    
    # Product details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    sku = Column(String(50), unique=True)
    
    # Pricing
    price = Column(Decimal(10, 2), nullable=False)
    purchase_price = Column(Decimal(10, 2))
    
    # Categorization
    family_id = Column(Integer, ForeignKey("product_families.id"))
    unit_id = Column(Integer, ForeignKey("units.id"))
    tax_rate_id = Column(Integer, ForeignKey("tax_rates.id"))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    family = relationship("ProductFamily")
    unit = relationship("Unit")
    tax_rate = relationship("TaxRate")

class ProductFamily(BaseModel):
    __tablename__ = "product_families"
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Relationships
    products = relationship("Product", back_populates="family")
```

## API Routes Migration

### 1. Invoice Routes Example
```python
# app/routers/invoices.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.invoice import Invoice, InvoiceStatus
from ..schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceResponse, InvoiceList
from ..services.invoice_service import InvoiceService
from ..dependencies import get_current_user, require_admin
from ..core.pagination import Paginated, paginate

router = APIRouter(prefix="/api/invoices", tags=["invoices"])

@router.get("/", response_model=Paginated[InvoiceList])
async def get_invoices(
    status: Optional[InvoiceStatus] = None,
    client_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get list of invoices with filtering and pagination"""
    query = db.query(Invoice)
    
    # Apply filters
    if status:
        query = query.filter(Invoice.status == status)
    if client_id:
        query = query.filter(Invoice.client_id == client_id)
    
    # Apply user-based filtering (non-admin users see only their invoices)
    if not current_user.is_admin:
        query = query.filter(Invoice.user_id == current_user.id)
    
    return paginate(query, page, size)

@router.post("/", response_model=InvoiceResponse)
async def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new invoice"""
    invoice_service = InvoiceService(db)
    return invoice_service.create_invoice(invoice_data, current_user.id)

@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get invoice by ID"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Check permissions
    if not current_user.is_admin and invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return invoice

@router.put("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: int,
    invoice_data: InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update an invoice"""
    invoice_service = InvoiceService(db)
    return invoice_service.update_invoice(invoice_id, invoice_data, current_user)

@router.delete("/{invoice_id}")
async def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete an invoice"""
    invoice_service = InvoiceService(db)
    invoice_service.delete_invoice(invoice_id, current_user)
    return {"message": "Invoice deleted successfully"}

@router.post("/{invoice_id}/send")
async def send_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Send invoice to client"""
    invoice_service = InvoiceService(db)
    return invoice_service.send_invoice(invoice_id, current_user)

@router.get("/{invoice_id}/pdf")
async def generate_invoice_pdf(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Generate and download invoice PDF"""
    from ..services.pdf_service import PDFService
    
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    pdf_service = PDFService()
    pdf_content = pdf_service.generate_invoice_pdf(invoice)
    
    from fastapi.responses import Response
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=invoice_{invoice.invoice_number}.pdf"}
    )
```

### 2. Client Routes Example
```python
# app/routers/clients.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.client import Client
from ..schemas.client import ClientCreate, ClientUpdate, ClientResponse, ClientList
from ..services.client_service import ClientService
from ..dependencies import get_current_user
from ..core.pagination import Paginated, paginate

router = APIRouter(prefix="/api/clients", tags=["clients"])

@router.get("/", response_model=Paginated[ClientList])
async def get_clients(
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get list of clients with search and filtering"""
    query = db.query(Client)
    
    # Apply filters
    if search:
        query = query.filter(
            (Client.name.contains(search)) |
            (Client.company.contains(search)) |
            (Client.email.contains(search))
        )
    
    if is_active is not None:
        query = query.filter(Client.is_active == is_active)
    
    return paginate(query.order_by(Client.name), page, size)

@router.post("/", response_model=ClientResponse)
async def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new client"""
    client_service = ClientService(db)
    return client_service.create_client(client_data)

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get client by ID"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a client"""
    client_service = ClientService(db)
    return client_service.update_client(client_id, client_data)
```

## Service Layer Migration

### Invoice Service Example
```python
# app/services/invoice_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.invoice import Invoice, InvoiceItem, InvoiceStatus
from ..models.client import Client
from ..schemas.invoice import InvoiceCreate, InvoiceUpdate
from ..core.exceptions import InvoiceNotFoundError, InvoiceValidationError
from ..services.email_service import EmailService
from ..services.pdf_service import PDFService
import uuid
from datetime import date, datetime

class InvoiceService:
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()
        self.pdf_service = PDFService()
    
    def create_invoice(self, invoice_data: InvoiceCreate, user_id: int) -> Invoice:
        """Create a new invoice"""
        # Validate client exists
        client = self.db.query(Client).filter(Client.id == invoice_data.client_id).first()
        if not client:
            raise InvoiceValidationError("Client not found")
        
        # Generate invoice number
        invoice_number = self._generate_invoice_number(invoice_data.invoice_group_id)
        
        # Create invoice
        invoice = Invoice(
            user_id=user_id,
            client_id=invoice_data.client_id,
            invoice_group_id=invoice_data.invoice_group_id,
            invoice_number=invoice_number,
            issue_date=invoice_data.issue_date or date.today(),
            due_date=invoice_data.due_date,
            terms=invoice_data.terms,
            notes=invoice_data.notes,
            url_key=uuid.uuid4().hex,
            status=InvoiceStatus.DRAFT
        )
        
        self.db.add(invoice)
        self.db.flush()  # Get the invoice ID
        
        # Add invoice items
        for item_data in invoice_data.items:
            item = InvoiceItem(
                invoice_id=invoice.id,
                name=item_data.name,
                description=item_data.description,
                quantity=item_data.quantity,
                price=item_data.price,
                product_id=item_data.product_id,
                tax_rate_id=item_data.tax_rate_id
            )
            self.db.add(item)
        
        self.db.commit()
        self.db.refresh(invoice)
        
        # Calculate totals
        self._calculate_invoice_totals(invoice)
        
        return invoice
    
    def update_invoice(self, invoice_id: int, invoice_data: InvoiceUpdate, current_user) -> Invoice:
        """Update an existing invoice"""
        invoice = self.db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise InvoiceNotFoundError("Invoice not found")
        
        # Check if invoice can be edited
        if invoice.status == InvoiceStatus.PAID:
            from ..core.config import settings
            if not settings.DISABLE_READ_ONLY:
                raise InvoiceValidationError("Cannot edit paid invoice")
        
        # Update invoice fields
        for field, value in invoice_data.dict(exclude_unset=True).items():
            if field != "items":
                setattr(invoice, field, value)
        
        # Update items if provided
        if invoice_data.items is not None:
            # Remove existing items
            self.db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()
            
            # Add new items
            for item_data in invoice_data.items:
                item = InvoiceItem(
                    invoice_id=invoice.id,
                    **item_data.dict()
                )
                self.db.add(item)
        
        invoice.updated_at = datetime.utcnow()
        self.db.commit()
        
        # Recalculate totals
        self._calculate_invoice_totals(invoice)
        
        return invoice
    
    def send_invoice(self, invoice_id: int, current_user) -> dict:
        """Send invoice to client via email"""
        invoice = self.db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise InvoiceNotFoundError("Invoice not found")
        
        if not invoice.client.email:
            raise InvoiceValidationError("Client has no email address")
        
        # Generate PDF
        pdf_content = self.pdf_service.generate_invoice_pdf(invoice)
        
        # Send email
        self.email_service.send_invoice_email(
            invoice=invoice,
            pdf_attachment=pdf_content
        )
        
        # Update invoice status
        if invoice.status == InvoiceStatus.DRAFT:
            invoice.status = InvoiceStatus.SENT
            self.db.commit()
        
        return {"message": "Invoice sent successfully"}
    
    def _generate_invoice_number(self, invoice_group_id: int) -> str:
        """Generate next invoice number for the group"""
        # Implementation similar to PHP version
        # This would query the invoice_groups table and increment the next_id
        pass
    
    def _calculate_invoice_totals(self, invoice: Invoice):
        """Calculate and update invoice totals"""
        subtotal = sum(item.quantity * item.price for item in invoice.items)
        tax_total = 0  # Calculate based on tax rates
        
        invoice.subtotal = subtotal
        invoice.tax_total = tax_total
        invoice.total = subtotal + tax_total
        invoice.balance = invoice.total - invoice.paid_amount
        
        self.db.commit()
```

## Configuration Migration

### Settings Configuration
```python
# app/config.py
from pydantic import BaseSettings, PostgresDsn, validator
from typing import Optional, Dict, Any
import secrets

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "InvoicePlane"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: PostgresDsn
    
    # JWT settings
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email settings
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    
    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Invoice settings
    LEGACY_CALCULATION: bool = True
    ENABLE_INVOICE_DELETION: bool = False
    DISABLE_READ_ONLY: bool = False
    
    # PDF settings
    PDF_ENGINE: str = "weasyprint"  # or "reportlab"
    
    # Localization
    DEFAULT_LANGUAGE: str = "en"
    DEFAULT_TIMEZONE: str = "UTC"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

## Authentication Migration

### JWT Authentication System
```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from ..config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .database import get_db
from .models.user import User
from .core.security import verify_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    payload = verify_token(credentials.credentials)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin privileges"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
```

## Migration Implementation Steps

### Phase 1: Core Infrastructure (Weeks 1-2)
1. **Project Setup**
   - Initialize FastAPI project structure
   - Set up database connection with SQLAlchemy
   - Configure Alembic for migrations
   - Set up testing framework

2. **Base Models**
   - Create base model class
   - Implement User model and authentication
   - Set up JWT authentication system

3. **Basic API Structure**
   - Create router structure
   - Implement basic CRUD operations
   - Set up API documentation

### Phase 2: Core Business Logic (Weeks 3-6)
1. **Client Management**
   - Migrate client model and routes
   - Implement client CRUD operations
   - Add client search and filtering

2. **Product Management**
   - Migrate product and product family models
   - Implement product CRUD operations
   - Add product categorization

3. **Invoice Core**
   - Migrate invoice and invoice item models
   - Implement basic invoice CRUD
   - Add invoice status management

### Phase 3: Advanced Features (Weeks 7-10)
1. **Invoice Advanced Features**
   - Invoice PDF generation
   - Email functionality
   - Recurring invoices
   - Invoice calculations and totals

2. **Payment System**
   - Payment tracking
   - Payment method management
   - Invoice payment reconciliation

3. **Project Management**
   - Project and task models
   - Time tracking integration
   - Project-to-invoice conversion

### Phase 4: Reporting & Advanced Features (Weeks 11-12)
1. **Reporting System**
   - Sales reports
   - Tax reports
   - Client reports
   - Custom report builder

2. **Advanced Features**
   - Custom fields system
   - Multi-language support
   - Import/export functionality
   - Archive management

### Phase 5: Frontend & Testing (Weeks 13-14)
1. **Frontend Integration**
   - Template migration to Jinja2
   - Static file management
   - Frontend API integration

2. **Testing & Documentation**
   - Comprehensive test suite
   - API documentation
   - Deployment documentation
   - Migration guide

## Dependencies and Requirements

### Core Dependencies
```txt
# requirements.txt
fastapi>=0.100.0
uvicorn[standard]>=0.22.0
sqlalchemy>=2.0.0
alembic>=1.11.0
psycopg2-binary>=2.9.0  # PostgreSQL driver
pymysql>=1.1.0          # MySQL driver (alternative)

# Authentication & Security
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6

# Data Validation
pydantic>=2.0.0
email-validator>=2.0.0

# PDF Generation
weasyprint>=59.0        # Modern PDF generation
# OR reportlab>=4.0.0   # Alternative PDF library

# Email
aiosmtplib>=2.0.0
jinja2>=3.1.0           # Template engine

# Utilities
python-dotenv>=1.0.0
celery>=5.3.0           # Background tasks
redis>=4.5.0            # Task queue backend

# Development & Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
httpx>=0.24.0           # Test client
black>=23.0.0           # Code formatting
flake8>=6.0.0           # Linting
mypy>=1.4.0             # Type checking
```

## Key Considerations

### 1. Data Migration Strategy
- Create migration scripts to convert existing PHP data
- Handle data type conversions (PHP arrays to JSON, etc.)
- Preserve all existing data integrity
- Create backup and rollback procedures

### 2. Backward Compatibility
- Maintain API compatibility where possible
- Support existing URL structures during transition
- Provide data export in original format

### 3. Performance Considerations
- Implement database indexing strategy
- Add query optimization
- Consider caching for frequently accessed data
- Implement pagination for large datasets

### 4. Security Enhancements
- Implement proper input validation
- Add rate limiting
- Enhance password security
- Add audit logging
- Implement CSRF protection

### 5. Testing Strategy
- Unit tests for all business logic
- Integration tests for API endpoints
- End-to-end tests for critical workflows
- Performance testing for large datasets

This migration plan provides a comprehensive roadmap for converting InvoicePlane from PHP to Python while maintaining all existing functionality and improving the overall architecture.
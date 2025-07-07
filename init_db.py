"""
Database initialization and seed data script
"""
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.base import Base
from app.models.user import User
from app.models.client import Client
from app.models.invoice import Invoice, InvoiceItem, InvoiceStatus
from app.core.security import get_password_hash
from datetime import date, timedelta
import uuid

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

def create_seed_data():
    """Create seed data for testing"""
    db = SessionLocal()
    try:
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@invoiceplane.com",
            hashed_password=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            is_active=True,
            is_admin=True
        )
        db.add(admin_user)
        db.flush()
        
        # Create regular user
        regular_user = User(
            username="user",
            email="user@invoiceplane.com",
            hashed_password=get_password_hash("user123"),
            first_name="John",
            last_name="Doe",
            is_active=True,
            is_admin=False
        )
        db.add(regular_user)
        db.flush()
        
        # Create sample clients
        client1 = Client(
            name="John",
            surname="Smith",
            company="ABC Corporation",
            email="john.smith@abc.com",
            phone="+1-555-0123",
            address_1="123 Business St",
            city="New York",
            state="NY",
            zip_code="10001",
            country="USA",
            is_active=True
        )
        db.add(client1)
        
        client2 = Client(
            name="Jane",
            surname="Johnson",
            company="XYZ Inc",
            email="jane@xyz.com",
            phone="+1-555-0456",
            address_1="456 Commerce Ave",
            city="Los Angeles",
            state="CA",
            zip_code="90210",
            country="USA",
            is_active=True
        )
        db.add(client2)
        
        client3 = Client(
            name="Bob",
            surname="Wilson",
            email="bob@example.com",
            phone="+1-555-0789",
            address_1="789 Main St",
            city="Chicago",
            state="IL",
            zip_code="60601",
            country="USA",
            is_active=True
        )
        db.add(client3)
        db.flush()
        
        # Create sample invoices
        invoice1 = Invoice(
            user_id=admin_user.id,
            client_id=client1.id,
            invoice_number="INV-2025-001",
            status=InvoiceStatus.SENT,
            issue_date=date.today() - timedelta(days=10),
            due_date=date.today() + timedelta(days=20),
            terms="Payment due within 30 days",
            notes="Thank you for your business!",
            url_key=uuid.uuid4().hex,
            subtotal=1000.00,
            tax_total=100.00,
            total=1100.00,
            paid_amount=0.00,
            balance=1100.00
        )
        db.add(invoice1)
        db.flush()
        
        # Add items to invoice1
        item1 = InvoiceItem(
            invoice_id=invoice1.id,
            name="Web Development Services",
            description="Custom website development",
            quantity=1,
            price=800.00,
            subtotal=800.00,
            total=800.00
        )
        db.add(item1)
        
        item2 = InvoiceItem(
            invoice_id=invoice1.id,
            name="SEO Optimization",
            description="Search engine optimization services",
            quantity=1,
            price=200.00,
            subtotal=200.00,
            total=200.00
        )
        db.add(item2)
        
        # Create more sample invoices
        invoice2 = Invoice(
            user_id=admin_user.id,
            client_id=client2.id,
            invoice_number="INV-2025-002",
            status=InvoiceStatus.PAID,
            issue_date=date.today() - timedelta(days=20),
            due_date=date.today() - timedelta(days=10),
            terms="Payment due within 30 days",
            url_key=uuid.uuid4().hex,
            subtotal=500.00,
            tax_total=50.00,
            total=550.00,
            paid_amount=550.00,
            balance=0.00
        )
        db.add(invoice2)
        db.flush()
        
        item3 = InvoiceItem(
            invoice_id=invoice2.id,
            name="Consulting Services",
            description="Business consultation",
            quantity=5,
            price=100.00,
            subtotal=500.00,
            total=500.00
        )
        db.add(item3)
        
        # Draft invoice
        invoice3 = Invoice(
            user_id=regular_user.id,
            client_id=client3.id,
            invoice_number="INV-2025-003",
            status=InvoiceStatus.DRAFT,
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            url_key=uuid.uuid4().hex,
            subtotal=750.00,
            tax_total=75.00,
            total=825.00,
            paid_amount=0.00,
            balance=825.00
        )
        db.add(invoice3)
        db.flush()
        
        item4 = InvoiceItem(
            invoice_id=invoice3.id,
            name="Design Services",
            description="Logo and branding design",
            quantity=1,
            price=750.00,
            subtotal=750.00,
            total=750.00
        )
        db.add(item4)
        
        db.commit()
        print("✅ Seed data created successfully")
        print("\n📋 Demo Credentials:")
        print("   Admin: admin / admin123")
        print("   User:  user / user123")
        
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Initializing InvoicePlane Python database...")
    create_tables()
    create_seed_data()
    print("✅ Database initialization complete!")

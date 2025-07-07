from sqlalchemy import Column, String, Text, Date, ForeignKey, Enum, Boolean, Integer, Numeric
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.models.base import BaseModel


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
    user_id = Column(ForeignKey("users.id"), nullable=False)
    client_id = Column(ForeignKey("clients.id"), nullable=False)
    
    # Invoice details
    invoice_number = Column(String(20), unique=True, nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    
    # Dates
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    
    # Content
    terms = Column(Text)
    notes = Column(Text)
    
    # Security
    url_key = Column(String(32), unique=True)
    
    # Calculated fields
    subtotal = Column(Numeric(10, 2), default=0)
    tax_total = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), default=0)
    paid_amount = Column(Numeric(10, 2), default=0)
    balance = Column(Numeric(10, 2), default=0)
    
    # Relationships
    client = relationship("Client", back_populates="invoices")
    user = relationship("User", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="invoice")
    
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
    invoice_id = Column(ForeignKey("invoices.id"), nullable=False)
    product_id = Column(ForeignKey("products.id"))
    
    # Item details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    quantity = Column(Numeric(10, 2), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    order = Column(Integer, default=0)
    
    # Calculated amounts
    subtotal = Column(Numeric(10, 2))
    tax_amount = Column(Numeric(10, 2))
    total = Column(Numeric(10, 2))
    
    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")
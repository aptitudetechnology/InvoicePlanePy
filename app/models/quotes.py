from sqlalchemy import Column, String, Text, Date, ForeignKey, Integer, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.models.base import BaseModel
from datetime import date

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
    
    # Invoice identification
    invoice_number = Column(String(20), unique=True, nullable=False)
    
    # Status (integer referencing the enum values above)
    status = Column(Integer, default=1)  # 1=DRAFT, 2=SENT, 3=VIEWED, 4=PAID, 5=OVERDUE, 6=CANCELLED
    
    # Dates
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    
    # Content
    terms = Column(Text)
    notes = Column(Text)
    
    # Security/sharing
    url_key = Column(String(32), unique=True)
    
    # Financial totals
    subtotal = Column(Numeric(10, 2), default=0.00)
    tax_total = Column(Numeric(10, 2), default=0.00)
    total = Column(Numeric(10, 2), default=0.00)
    paid_amount = Column(Numeric(10, 2), default=0.00)
    balance = Column(Numeric(10, 2), default=0.00)
    
    # Timestamps (likely inherited from BaseModel, but including for reference)
    # created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    # updated_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    user = relationship("User", back_populates="invoices")
    client = relationship("Client", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    
    @property
    def status_name(self) -> str:
        """Get status name from enum"""
        try:
            return InvoiceStatus(self.status).name
        except ValueError:
            return "UNKNOWN"
    
    @property
    def is_overdue(self) -> bool:
        """Check if invoice is overdue"""
        return (self.status not in [InvoiceStatus.PAID.value, InvoiceStatus.CANCELLED.value] 
                and self.due_date < date.today())
    
    @property
    def days_overdue(self) -> int:
        """Calculate days overdue (negative if not yet due)"""
        return (date.today() - self.due_date).days
    
    @property
    def is_paid(self) -> bool:
        """Check if invoice is fully paid"""
        return self.status == InvoiceStatus.PAID.value or self.balance <= 0
    
    @property
    def can_be_cancelled(self) -> bool:
        """Check if invoice can be cancelled"""
        return self.status in [InvoiceStatus.DRAFT.value, InvoiceStatus.SENT.value]

class InvoiceItem(BaseModel):
    __tablename__ = "invoice_items"
    
    # Foreign keys
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    
    # Item details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    quantity = Column(Numeric(10, 2), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    
    # Ordering (note: "order" is a reserved word, so it's quoted in the schema)
    order = Column("order", Integer, default=0)
    
    # Calculated amounts
    subtotal = Column(Numeric(10, 2))
    tax_amount = Column(Numeric(10, 2))
    total = Column(Numeric(10, 2))
    
    # Timestamps (likely inherited from BaseModel)
    # created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    # updated_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")
    
    @property
    def line_total(self) -> float:
        """Calculate line total (quantity * price)"""
        if self.quantity and self.price:
            return float(self.quantity * self.price)
        return 0.0
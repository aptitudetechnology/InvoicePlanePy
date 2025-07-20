from sqlalchemy import Column, String, Text, Date, ForeignKey, Enum, Boolean, Integer, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.models.base import BaseModel
from datetime import date

class QuoteStatus(PyEnum):
    DRAFT = 'DRAFT'
    SENT = 'SENT'
    VIEWED = 'VIEWED'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    EXPIRED = 'EXPIRED'
    CONVERTED = 'CONVERTED'  # When quote becomes an invoice

class Quote(BaseModel):
    __tablename__ = "quotes"
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    # Quote identification and details
    quote_number = Column(String(50), nullable=False, unique=True)
    title = Column(String(255))
    issue_date = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=True)
    
    # Financial fields
    total = Column(Numeric(10, 2), nullable=False)
    balance = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default='AUD')
    
    # Tax and discount
    tax_rate = Column(Numeric(5, 2), default=0.00)
    tax_amount = Column(Numeric(10, 2))
    discount_percentage = Column(Numeric(5, 2), default=0.00)
    
    # Status - references quote_statuses table
    status = Column(Integer, ForeignKey("quote_statuses.id"), nullable=False)
    
    # Content
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    
    # Relationships
    client = relationship("Client", back_populates="quotes")
    user = relationship("User", back_populates="quotes")
    items = relationship("QuoteItem", back_populates="quote", cascade="all, delete-orphan")
    
    @property
    def is_expired(self) -> bool:
        """Check if quote is expired"""
        if not self.valid_until:
            return False
        return (self.status not in [QuoteStatus.DRAFT, QuoteStatus.ACCEPTED, QuoteStatus.CONVERTED]
                and self.valid_until < date.today())
    
    @property
    def days_until_expiry(self) -> int:
        """Calculate days until expiry (negative if expired)"""
        if not self.valid_until:
            return 999  # No expiry date set
        return (self.valid_until - date.today()).days
    
    @property
    def can_be_converted(self) -> bool:
        """Check if quote can be converted to invoice"""
        return self.status == QuoteStatus.ACCEPTED

class QuoteItem(BaseModel):
    __tablename__ = "quote_items"
    
    # Foreign keys
    quote_id = Column(Integer, ForeignKey("quotes.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    
    # Item details
    product_name = Column(String(255))
    description = Column(Text)
    unit_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    
    # Discount and tax
    discount_percentage = Column(Numeric(5, 2), default=0.00)
    tax_rate = Column(Numeric(5, 2), default=0.00)
    tax_amount = Column(Numeric(10, 2))
    discount_amount = Column(Numeric(10, 2))
    
    # Calculated amounts
    subtotal = Column(Numeric(10, 2))
    total = Column(Numeric(10, 2))
    
    # Ordering
    sort_order = Column(Integer)
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    
    # Relationships
    quote = relationship("Quote", back_populates="items")
    product = relationship("Product")
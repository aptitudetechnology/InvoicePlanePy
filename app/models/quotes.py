from sqlalchemy import Column, String, Text, Date, ForeignKey, Enum, Boolean, Integer, Numeric
from sqlalchemy.orm import relationship
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
    user_id = Column(ForeignKey("users.id"), nullable=False)
    client_id = Column(ForeignKey("clients.id"), nullable=False)
    
    # Quote details - REMOVED product_name (it belongs to quote_items)
    #description = Column(Text)
    quantity = Column(Numeric(10, 3), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    issue_date = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=True)
    
    # Discount and tax fields for template support
    discount_percentage = Column(Numeric(5, 2), default=0.00)
    tax_rate = Column(Numeric(5, 2), default=0.00)
    tax_amount = Column(Numeric(10, 2), default=0.00)
    discount_amount = Column(Numeric(10, 2), default=0.00)
    
    # Content
    terms = Column(Text)
    notes = Column(Text)
    
    # Security
    url_key = Column(String(32), unique=True)
    
    # Calculated fields
    subtotal = Column(Numeric(10, 2), default=0)
    tax_total = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), default=0)
    
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
    quote_id = Column(ForeignKey("quotes.id"), nullable=False)
    product_id = Column(ForeignKey("products.id"))
    
    # Item details - FIXED to match database schema
    product_name = Column(String(255))  # Changed from 'name' to 'product_name'
    description = Column(Text)
    unit_price = Column(Numeric(10, 2), nullable=False)  # Changed from 'price' to 'unit_price'
    quantity = Column(Numeric(10, 2), nullable=False)
    discount_percentage = Column(Numeric(5, 2), default=0.00)  # Added from schema
    tax_rate = Column(Numeric(5, 2), default=0.00)  # Added from schema
    sort_order = Column(Integer)  # Removed default=0 to match schema
    
    # Calculated amounts
    tax_amount = Column(Numeric(10, 2))
    subtotal = Column(Numeric(10, 2))
    discount_amount = Column(Numeric(10, 2))  # Added from schema
    total = Column(Numeric(10, 2))
    
    # Relationships
    quote = relationship("Quote", back_populates="items")
    product = relationship("Product")
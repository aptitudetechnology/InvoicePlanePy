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

class Quote(BaseModel):  # Changed from Quotes to Quote
    __tablename__ = "quotes"
    
    # Foreign keys
    user_id = Column(ForeignKey("users.id"), nullable=False)
    client_id = Column(ForeignKey("clients.id"), nullable=False)
    
    # Quote details
    quote_number = Column(String(20), unique=True, nullable=False)
    status = Column(Enum(QuoteStatus), default=QuoteStatus.DRAFT)
    
    # Dates
    issue_date = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=True)
    
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
    quote = relationship("Quote", back_populates="items")  # Changed from Quotes to Quote
    product = relationship("Product")
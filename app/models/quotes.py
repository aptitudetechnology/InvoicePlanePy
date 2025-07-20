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
    CONVERTED = 'CONVERTED' # When quote becomes an invoice

class Quote(BaseModel):
    __tablename__ = "quotes"
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    # Quote details - exactly matching your database schema
    quote_number = Column(String(50), nullable=False, unique=True)
    #title = Column(String(255))
    issue_date = Column(Date, nullable=False)
    valid_until = Column(Date)
    
    # Financial fields - exactly matching your database schema
    total = Column(Numeric(10, 2), nullable=False)
    #balance = Column(Numeric(10, 2), nullable=False)
    #currency = Column(String(3), default='AUD')
    tax_rate = Column(Numeric(5, 2), default=0.00)
    tax_amount = Column(Numeric(10, 2))
    
    # Content
    notes = Column(Text)
    
    # Status - Integer FK to quote_statuses table
    status = Column(Integer, ForeignKey("quote_statuses.id"), nullable=False)
    
    # Relationships
    client = relationship("Client", back_populates="quotes")
    user = relationship("User", back_populates="quotes")
    items = relationship("QuoteItem", back_populates="quote", cascade="all, delete-orphan")
    
    @property
    def is_expired(self) -> bool:
        """Check if quote is expired"""
        if not self.valid_until:
            return False
        # You'll need to map status IDs to their meanings
        # This assumes non-active statuses, adjust based on your quote_statuses table
        return (self.status not in [1, 4, 7]  # Update with actual status IDs
                and self.valid_until < date.today())
    
    @property
    def days_until_expiry(self) -> int:
        """Calculate days until expiry (negative if expired)"""
        if not self.valid_until:
            return 999 # No expiry date set
        return (self.valid_until - date.today()).days
    
    @property
    def can_be_converted(self) -> bool:
        """Check if quote can be converted to invoice"""
        # Update with the actual status ID for ACCEPTED in your quote_statuses table
        return self.status == 4  # Adjust this based on your quote_statuses table

class QuoteItem(BaseModel):
    __tablename__ = "quote_items"
    
    # Foreign keys
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    
    # Item details - exactly matching your database schema.
    product_name = Column(String(255))
    description = Column(Text)
    unit_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    discount_percentage = Column(Numeric(5, 2), default=0.00)
    tax_rate = Column(Numeric(5, 2), default=0.00)
    sort_order = Column(Integer)
    
    # Calculated amounts - exactly matching your database schema
    tax_amount = Column(Numeric(10, 2))
    subtotal = Column(Numeric(10, 2))
    discount_amount = Column(Numeric(10, 2))
    total = Column(Numeric(10, 2))
    
    # Relationships
    quote = relationship("Quote", back_populates="items")
    product = relationship("Product")
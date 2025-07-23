# Assuming this file is your models/quote.py or part of a main models.py

from sqlalchemy import Column, String, Text, Date, ForeignKey, Enum, Boolean, Integer, Numeric
from sqlalchemy.orm import relationship # Ensure relationship is imported
from enum import Enum as PyEnum
from app.models.base import BaseModel # Keep this import
from datetime import date

# --- NEW: Import the QuoteStatusModel ---
# Adjust this import path if QuoteStatusModel is in a different file or the same as this one.
# For example, if QuoteStatusModel is in app/models/quote_status.py:
from app.models.quote_status import QuoteStatusModel
# If QuoteStatusModel is in the *same* file as this Quote model, you don't need this specific import,
# but rather just ensure QuoteStatusModel is defined before Quote.

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
    #tax_rate = Column(Numeric(5, 2), default=0.00)
    #tax_amount = Column(Numeric(10, 2))


    # Content
    notes = Column(Text)
   #terms = Column(Text, nullable=True)  # Added to support 'terms' field

    # Status - Integer FK to quote_statuses table
    status = Column(Integer, ForeignKey("quote_statuses.id"), nullable=False)

    # --- NEW: Add the ORM relationship to QuoteStatusModel ---
    # This creates a 'status_object' attribute on your Quote instance
    # allowing you to access the related QuoteStatusModel object.
    status_object = relationship("QuoteStatusModel") # Make sure "QuoteStatusModel" matches the class name you defined

    # Relationships
    client = relationship("Client", back_populates="quotes")
    user = relationship("User", back_populates="quotes")
    items = relationship("QuoteItem", back_populates="quote", cascade="all, delete-orphan")

    @property
    def is_expired(self) -> bool:
        """Check if quote is expired"""
        if not self.valid_until:
            return False
        # --- UPDATED: Use the relationship for more robust status checking ---
        # Ensure your 'quote_statuses' table is populated with the 'name' values
        # corresponding to your PyEnum members.
        if not self.status_object: # Handle case where status_object might not be loaded/present
            return False # Or raise an error, depending on your desired behavior

        return (self.status_object.name not in [QuoteStatus.ACCEPTED.value, QuoteStatus.CONVERTED.value]
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
        # --- UPDATED: Use the relationship for more robust status checking ---
        if not self.status_object:
            return False
        return self.status_object.name == QuoteStatus.ACCEPTED.value

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
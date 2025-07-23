# app/models/quote_status.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from app.models.base import BaseModel # Assuming BaseModel is located here

class QuoteStatusModel(BaseModel):
    """
    SQLAlchemy ORM model for the 'quote_statuses' database table.
    This table stores the various possible statuses a quote can have.
    """
    __tablename__ = "quote_statuses"

    id = Column(Integer, primary_key=True, autoincrement=True) # Corresponds to SERIAL PRIMARY KEY
    name = Column(String(50), nullable=False, unique=True) # Corresponds to VARCHAR(50) NOT NULL UNIQUE
    description = Column(Text) # Corresponds to TEXT
    is_active = Column(Boolean, default=True) # Corresponds to BOOLEAN DEFAULT TRUE
    created_at = Column(DateTime, default=datetime.utcnow) # Corresponds to TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # Corresponds to TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    def __repr__(self):
        return f"<QuoteStatusModel(id={self.id}, name='{self.name}', is_active={self.is_active})>"
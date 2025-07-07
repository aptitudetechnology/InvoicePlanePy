from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    # Basic fields
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile fields
    first_name = Column(String(50))
    last_name = Column(String(50))
    company = Column(String(100))
    
    # Status fields
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Last login tracking
    last_login = Column(DateTime)
    
    # Relationships
    invoices = relationship("Invoice", back_populates="user")
    quotes = relationship("Quote", back_populates="user")
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = func.now()

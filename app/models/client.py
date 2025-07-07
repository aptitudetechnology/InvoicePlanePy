from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Client(BaseModel):
    __tablename__ = "clients"
    
    # Core fields
    name = Column(String(100), nullable=False)
    surname = Column(String(100))
    title = Column(String(50))
    company = Column(String(255))
    
    # Contact information
    email = Column(String(100))
    phone = Column(String(20))
    mobile = Column(String(20))
    fax = Column(String(20))
    website = Column(String(100))
    
    # Address fields
    address_1 = Column(String(100))
    address_2 = Column(String(100))
    city = Column(String(45))
    state = Column(String(35))
    zip_code = Column(String(15))
    country = Column(String(35))
    
    # Business details
    vat_id = Column(String(50))
    tax_code = Column(String(50))
    
    # Status and settings
    is_active = Column(Boolean, default=True)
    language = Column(String(10), default='en')
    
    # Notes
    notes = Column(Text)
    
    # Relationships
    invoices = relationship("Invoice", back_populates="client")
    quotes = relationship("Quote", back_populates="client")
    projects = relationship("Project", back_populates="client")
    
    @property
    def full_name(self) -> str:
        """Get client's full name"""
        if self.surname:
            return f"{self.name} {self.surname}"
        return self.name
    
    @property
    def display_name(self) -> str:
        """Get display name (company or full name)"""
        return self.company if self.company else self.full_name

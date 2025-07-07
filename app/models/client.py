from sqlalchemy import Column, String, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Client(BaseModel):
    __tablename__ = "clients"
    
    # Foreign key to user who owns this client
    user_id = Column(ForeignKey("users.id"), nullable=False)
    
    # Personal Information
    is_active = Column(Boolean, default=True)
    name = Column(String(100), nullable=False)  # Client Name
    surname = Column(String(100))  # Client Surname (Optional)
    language = Column(String(10), default='en')
    
    # Address
    address_1 = Column(String(255))  # Street Address
    address_2 = Column(String(255))  # Street Address 2
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    country = Column(String(50))
    
    # Contact Information
    phone = Column(String(20))  # Phone Number
    fax = Column(String(20))    # Fax Number
    mobile = Column(String(20)) # Mobile Number
    email = Column(String(100)) # Email Address
    website = Column(String(255))  # Web Address
    
    # Personal Information (Additional)
    gender = Column(String(10))  # Gender
    birthdate = Column(Date)     # Birthdate
    company = Column(String(255)) # Company Name
    
    # Taxes Information
    vat_id = Column(String(50))   # VAT ID
    tax_code = Column(String(50)) # Taxes Code
    abn = Column(String(50))      # ABN (Australian Business Number)
    
    # Legacy fields for compatibility
    title = Column(String(50))
    
    # Notes
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="clients")
    invoices = relationship("Invoice", back_populates="client")
    # quotes = relationship("Quote", back_populates="client")  # TODO: Create Quote model
    projects = relationship("Project", back_populates="client")
    tasks = relationship("Task", back_populates="client")
    
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

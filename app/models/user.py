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
    role = Column(String(20), default="user")  # user, admin, manager
    language = Column(String(10), default="en")
    
    # Address fields
    street_address = Column(String(255))
    street_address_2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    country = Column(String(10))  # ISO country code
    
    # Tax information fields
    vat_id = Column(String(50))
    tax_code = Column(String(50))
    iban = Column(String(50))
    acn = Column(String(50))  # Australian Company Number
    abn = Column(String(50))  # Australian Business Number
    subscriber_number = Column(String(50))
    
    # Contact information fields
    phone_number = Column(String(20))
    fax_number = Column(String(20))
    mobile_number = Column(String(20))
    web_address = Column(String(255))
    
    # Status fields
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Last login tracking
    last_login = Column(DateTime)
    
    # Relationships
    invoices = relationship("Invoice", back_populates="user")
    # quotes = relationship("Quote", back_populates="user")  # TODO: Create Quote model
    products = relationship("Product", back_populates="user")
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = func.now()

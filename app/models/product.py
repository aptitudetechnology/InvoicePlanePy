from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"
    
    # Product details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    sku = Column(String(50), unique=True)
    
    # Foreign keys
    user_id = Column(ForeignKey("users.id"), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="products")

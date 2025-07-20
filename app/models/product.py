from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ProductFamily(BaseModel):
    __tablename__ = "product_families"
    
    # Family details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    products = relationship("Product", back_populates="family")


class ProductUnit(BaseModel):
    __tablename__ = "product_units"
    
    # Unit details
    name = Column(String(50), nullable=False)
    abbreviation = Column(String(10), nullable=False)
    description = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    products = relationship("Product", back_populates="unit")


class Product(BaseModel):
    __tablename__ = "products"
    
    # Product details
    name = Column(String(255), nullable=False)  # Updated length to 255
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)  # Changed to nullable=True
    sku = Column(String(100), unique=True, nullable=False)  # Updated length and made required
    tax_rate = Column(Numeric(5, 2), default=0.00)

    # Foreign keys
    user_id = Column(ForeignKey("users.id"), nullable=True)
    family_id = Column(ForeignKey("product_families.id"), nullable=True)
    unit_id = Column(ForeignKey("product_units.id"), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)  # Changed from is_active to active
    
    # Relationships
    user = relationship("User", back_populates="products")
    family = relationship("ProductFamily", back_populates="products")
    unit = relationship("ProductUnit", back_populates="products")
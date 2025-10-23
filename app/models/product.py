from sqlalchemy import Column, String, Text, Numeric, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ProductFamily(BaseModel):
    __tablename__ = "ip_families"
    
    # Override the default id column name to match PHP
    id = Column("family_id", Integer, primary_key=True, autoincrement=True)
    
    # Family details
    name = Column("family_name", String(100), nullable=False)
    description = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    products = relationship("Product", back_populates="family")


class ProductUnit(BaseModel):
    __tablename__ = "ip_units"
    
    # Override the default id column name to match PHP
    id = Column("unit_id", Integer, primary_key=True, autoincrement=True)
    
    # Unit details
    name = Column("unit_name", String(50), nullable=False)
    abbreviation = Column("unit_name_plrl", String(10), nullable=False)
    description = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    products = relationship("Product", back_populates="unit")


class Product(BaseModel):
    __tablename__ = "ip_products"
    
    # Override the default id column name to match PHP
    id = Column("product_id", Integer, primary_key=True, autoincrement=True)
    
    # Product details
    name = Column("product_name", String(255), nullable=False)
    description = Column("product_description", Text, nullable=True)
    price = Column("product_price", Numeric(10, 2), nullable=True)
    sku = Column("product_sku", String(100), unique=True, nullable=False)
    tax_rate = Column(Numeric(5, 2), default=0.00)
    
    # Additional optional fields
    provider_name = Column(String(255), nullable=True)
    purchase_price = Column(Numeric(10, 2), nullable=True)
    sumex = Column(Boolean, default=False)
    tariff = Column("product_tariff", Numeric(10, 2), nullable=True)

    # Foreign keys
    user_id = Column(ForeignKey("users.id"), nullable=True)
    family_id = Column(ForeignKey("ip_families.family_id"), nullable=True)
    unit_id = Column(ForeignKey("ip_units.unit_id"), nullable=True)
    tax_rate_id = Column(ForeignKey("ip_tax_rates.tax_rate_id"), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="products")
    family = relationship("ProductFamily", back_populates="products")
    unit = relationship("ProductUnit", back_populates="products")
    tax_rate_rel = relationship("TaxRate", back_populates="products")
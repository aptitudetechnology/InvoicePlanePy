from sqlalchemy import Column, String, Float, Boolean, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class TaxRate(BaseModel):
    __tablename__ = "ip_tax_rates"
    
    # Override the default id column name to match PHP
    id = Column("tax_rate_id", Integer, primary_key=True, autoincrement=True)

    name = Column("tax_rate_name", String(100), nullable=False, unique=True)
    rate = Column("tax_rate_percent", Float, nullable=False)
    is_default = Column(Boolean, default=False)

    # Relationships
    products = relationship("Product", back_populates="tax_rate_rel")

    def __repr__(self):
        return f"<TaxRate(id={self.id}, name='{self.name}', rate={self.rate}%)>"
# app/models/tax_rate.py
from sqlalchemy import Column, String, Float, Boolean
from app.models.base import BaseModel

class TaxRate(BaseModel):
    __tablename__ = "tax_rates"

    name = Column(String(100), nullable=False, unique=True)
    rate = Column(Float, nullable=False)
    is_default = Column(Boolean, default=False)

    def __repr__(self):
        return f"<TaxRate(id={self.id}, name='{self.name}', rate={self.rate}%)>"
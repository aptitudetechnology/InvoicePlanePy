from sqlalchemy import Column, String, Date, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Payment(BaseModel):
    __tablename__ = "payments"
    
    # Foreign keys
    invoice_id = Column(ForeignKey("invoices.id"), nullable=False)
    
    # Payment details
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String(50))
    reference_number = Column(String(100))
    notes = Column(Text)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="payments")

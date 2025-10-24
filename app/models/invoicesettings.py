from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric
from app.models.base import BaseModel

class InvoiceSettings(BaseModel):
    __tablename__ = "invoice_settings"

    id = Column(Integer, primary_key=True)
    default_invoice_group = Column(String(50), nullable=True)
    default_invoice_terms = Column(Text, nullable=True)
    invoice_default_payment_method = Column(String(50), nullable=True)
    invoices_due_after = Column(Integer, nullable=True)
    generate_invoice_number_for_draft = Column(Boolean, default=False)
    einvoicing = Column(Boolean, default=False)
    pdf_invoice_footer = Column(Text, nullable=True)
    pdf_template = Column(String(100), nullable=True)
    invoice_logo = Column(String(255), nullable=True)
    invoice_pdf_password = Column(String(255), nullable=True)
    enable_pdf_watermarks = Column(Boolean, default=False)
    include_zugferd = Column(Boolean, default=False)

    # Add other fields as needed from legacy or new requirements

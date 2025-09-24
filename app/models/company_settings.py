from sqlalchemy import Column, Integer, String, Text, Boolean
from app.models.base import BaseModel

class CompanySettings(BaseModel):
    __tablename__ = "company_settings"

    id = Column(Integer, primary_key=True)
    language = Column(String(50), default="english")
    theme = Column(String(100), default="invoiceplane-default")
    first_day_week = Column(String(20), default="monday")
    date_format = Column(String(20), default="m/d/Y")
    default_country = Column(String(10), default="US")
    items_per_page = Column(Integer, default=25)
    currency_symbol = Column(String(10), default="$")
    currency_placement = Column(String(20), default="before")
    currency_code = Column(String(10), default="USD")
    tax_decimal_places = Column(Integer, default=2)
    number_format = Column(String(20), default="comma_dot")
    company_name = Column(String(255), nullable=True)
    company_address = Column(Text, nullable=True)
    company_address_2 = Column(Text, nullable=True)
    company_city = Column(String(255), nullable=True)
    company_state = Column(String(255), nullable=True)
    company_zip = Column(String(20), nullable=True)
    company_country = Column(String(10), nullable=True)
    company_phone = Column(String(50), nullable=True)
    company_email = Column(String(255), nullable=True)
    default_invoice_tax = Column(String(50), default="none")
    default_invoice_tax_placement = Column(String(20), default="after")
    default_item_tax = Column(String(50), default="none")
from pydantic import BaseSettings
from typing import Optional
import secrets

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "InvoicePlane Python"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://invoiceplane:password@localhost:5432/invoiceplane"
    
    # JWT settings
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email settings
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    
    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Invoice settings
    LEGACY_CALCULATION: bool = True
    ENABLE_INVOICE_DELETION: bool = False
    DISABLE_READ_ONLY: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

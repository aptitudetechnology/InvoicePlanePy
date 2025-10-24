# Test script for SystemSetting model and settings persistence
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.system_setting import SystemSetting

# Use your actual database URL or a SQLite test DB
DATABASE_URL = "sqlite:///test_settings.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

def set_setting(db, key, value):
    setting = db.query(SystemSetting).filter_by(key=key).first()
    if setting:
        setting.value = value
    else:
        setting = SystemSetting(key=key, value=value)
        db.add(setting)
    db.commit()

def get_settings(db):
    return {s.key: s.value for s in db.query(SystemSetting).all()}

def test_settings():
    db = SessionLocal()
    print("Setting test values...")
    set_setting(db, "default_invoice_group", "monthly")
    set_setting(db, "default_payment_method", "cash")
    set_setting(db, "default_terms", "Please pay within 7 days.")
    set_setting(db, "invoices_due_after", "7")
    set_setting(db, "generate_invoice_number_draft", "yes")
    set_setting(db, "mark_invoices_sent_pdf", "no")
    set_setting(db, "enable_pdf_watermarks", "yes")
    set_setting(db, "invoice_pdf_password", "secret")
    set_setting(db, "include_zugferd", "no")
    set_setting(db, "default_pdf_template", "modern-template")
    print("Fetching settings from DB...")
    settings = get_settings(db)
    for k, v in settings.items():
        print(f"{k}: {v}")
    db.close()

if __name__ == "__main__":
    test_settings()

#!/usr/bin/env python3
"""
Create company_settings table and populate initial data
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, '/app')

try:
    from app.database import SessionLocal, engine
    from app.models.company_settings import CompanySettings
    from sqlalchemy import text

    def main():
        print("🔧 Creating company_settings table...")
        
        # Create the table
        CompanySettings.__table__.create(bind=engine, checkfirst=True)
        print("✅ company_settings table created")
        
        # Check if settings already exist
        db = SessionLocal()
        try:
            settings = db.query(CompanySettings).first()
            if settings:
                print("✅ Company settings already exist")
            else:
                # Create default settings
                default_settings = CompanySettings()
                db.add(default_settings)
                db.commit()
                print("✅ Default company settings created")
                
        except Exception as e:
            print(f"❌ Error with settings: {e}")
            db.rollback()
        finally:
            db.close()

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this inside the Docker container")
    sys.exit(1)
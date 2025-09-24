#!/usr/bin/env python3
"""
Check and populate tax rates in the database for Docker environment
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, '/app')

try:
    from app.database import SessionLocal
    from app.models.tax_rate import TaxRate

    def main():
        print("🔍 Checking tax rates in database...")
        db = SessionLocal()
        try:
            # Check existing tax rates
            tax_rates = db.query(TaxRate).all()
            print(f"Found {len(tax_rates)} tax rates in database:")

            for tr in tax_rates:
                print(f"  {tr.id}: {tr.name} ({tr.rate}%)")

            # If no tax rates exist, create some defaults
            if not tax_rates:
                print("\n❌ No tax rates found. Creating default tax rates...")

                default_rates = [
                    {"name": "GST", "rate": 10.0},
                    {"name": "VAT", "rate": 20.0},
                    {"name": "Sales Tax", "rate": 8.5},
                ]

                for rate_data in default_rates:
                    tax_rate = TaxRate(**rate_data)
                    db.add(tax_rate)
                    print(f"✅ Created: {rate_data['name']} ({rate_data['rate']}%)")

                db.commit()
                print("🎉 Default tax rates created successfully!")
                print("Please refresh your quote editing page to see the populated dropdowns.")

            else:
                print("\n✅ Tax rates already exist.")

        except Exception as e:
            print(f"❌ Error: {e}")
            db.rollback()
        finally:
            db.close()

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this inside the Docker container with the app mounted at /app")
    sys.exit(1)
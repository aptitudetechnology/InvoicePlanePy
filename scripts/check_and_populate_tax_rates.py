#!/usr/bin/env python3
"""
Check and populate tax rates in the database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.tax_rate import TaxRate

def main():
    db = SessionLocal()
    try:
        # Check existing tax rates
        tax_rates = db.query(TaxRate).all()
        print(f"Found {len(tax_rates)} tax rates in database:")

        for tr in tax_rates:
            print(f"  {tr.id}: {tr.name} ({tr.rate}%)")

        # If no tax rates exist, create some defaults
        if not tax_rates:
            print("\nNo tax rates found. Creating default tax rates...")

            default_rates = [
                {"name": "GST", "rate": 10.0},
                {"name": "VAT", "rate": 20.0},
                {"name": "Sales Tax", "rate": 8.5},
            ]

            for rate_data in default_rates:
                tax_rate = TaxRate(**rate_data)
                db.add(tax_rate)
                print(f"Created: {rate_data['name']} ({rate_data['rate']}%)")

            db.commit()
            print("Default tax rates created successfully!")

        else:
            print("\nTax rates already exist.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
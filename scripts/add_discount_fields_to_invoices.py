#!/usr/bin/env python3
"""
Add discount fields to invoices table
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, '/app')

try:
    from app.database import engine
    from sqlalchemy import text

    def main():
        print("🔧 Adding discount fields to invoices table...")

        # Add discount_amount column to invoices
        try:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE invoices ADD COLUMN IF NOT EXISTS discount_amount NUMERIC(10,2) DEFAULT 0"))
                conn.execute(text("ALTER TABLE invoices ADD COLUMN IF NOT EXISTS discount_percentage NUMERIC(5,2) DEFAULT 0"))
                conn.execute(text("ALTER TABLE invoice_items ADD COLUMN IF NOT EXISTS discount_amount NUMERIC(10,2) DEFAULT 0"))
                conn.commit()
            print("✅ Discount fields added to invoices and invoice_items tables")
        except Exception as e:
            print(f"❌ Error adding discount fields: {e}")
            return 1

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this inside the Docker container")
    sys.exit(1)
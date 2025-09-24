#!/usr/bin/env python3
"""
Simple script to check and populate tax rates using direct SQL
"""

import os
import psycopg2
from urllib.parse import urlparse

def get_database_url():
    """Get DATABASE_URL from environment"""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        # Try common defaults for Docker
        database_url = "postgresql://invoiceplane:password@db:5432/invoiceplane"
    return database_url

def main():
    database_url = get_database_url()
    print(f"🔍 Connecting to database: {database_url}")

    try:
        # Parse URL and connect
        url = urlparse(database_url)
        conn = psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cur = conn.cursor()

        # Check existing tax rates
        cur.execute("SELECT COUNT(*) FROM tax_rate")
        count = cur.fetchone()[0]
        print(f"Found {count} tax rates in database")

        if count == 0:
            print("❌ No tax rates found. Creating defaults...")

            # Create default tax rates
            default_rates = [
                ("GST", 10.0),
                ("VAT", 20.0),
                ("Sales Tax", 8.5),
            ]

            for name, rate in default_rates:
                cur.execute(
                    "INSERT INTO tax_rate (name, rate) VALUES (%s, %s)",
                    (name, rate)
                )
                print(f"✅ Created: {name} ({rate}%)")

            conn.commit()
            print("🎉 Default tax rates created successfully!")
        else:
            # Show existing rates
            cur.execute("SELECT id, name, rate FROM tax_rate ORDER BY name")
            rows = cur.fetchall()
            print("Existing tax rates:")
            for row in rows:
                print(f"  {row[0]}: {row[1]} ({row[2]}%)")

        cur.close()
        conn.close()
        print("✅ Database connection closed")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
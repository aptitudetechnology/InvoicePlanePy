#!/usr/bin/env python3
"""
Check the current api_keys table schema
"""
from app.database import engine
from sqlalchemy import text

def check_api_keys_schema():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'api_keys'
            ORDER BY ordinal_position
        """))
        print("Current api_keys table columns:")
        for row in result:
            print(f"  {row[0]}: {row[1]} {'NULL' if row[2] == 'YES' else 'NOT NULL'}")

if __name__ == "__main__":
    check_api_keys_schema()
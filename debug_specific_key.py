#!/usr/bin/env python3
"""
Debug API key authentication for a specific key
"""
import hashlib
from app.database import engine
from sqlalchemy import text

def debug_specific_api_key():
    """Check if a specific API key exists in the database"""
    test_key = "sk_l94N4oxt1fA8lrW3gRF9SkGHMzN-fr4a5DCW5PlMEXk"

    # Calculate the expected hash
    expected_hash = hashlib.sha256(test_key.encode()).hexdigest()
    print(f"API Key: {test_key}")
    print(f"Expected Hash: {expected_hash}")
    print(f"Key Prefix: {test_key[:8]}")

    # Check database
    with engine.connect() as conn:
        # Check if the hash exists
        result = conn.execute(text("""
            SELECT id, key_prefix, name, is_active, created_at, last_used_at
            FROM api_keys
            WHERE key_hash = :hash
        """), {"hash": expected_hash})

        row = result.fetchone()
        if row:
            print("✅ Key found in database!")
            print(f"ID: {row[0]}, Prefix: {row[1]}, Name: {row[2]}, Active: {row[3]}")
            print(f"Created: {row[4]}, Last Used: {row[5]}")
        else:
            print("❌ Key NOT found in database")

        # Show all API keys for reference
        print("\nAll API keys in database:")
        result = conn.execute(text("""
            SELECT id, key_prefix, name, is_active, created_at, last_used_at
            FROM api_keys
            ORDER BY created_at DESC
        """))

        for row in result:
            print(f"ID: {row[0]}, Prefix: {row[1]}, Name: {row[2]}, Active: {row[3]}, Created: {row[4]}, Last Used: {row[5]}")

if __name__ == "__main__":
    debug_specific_api_key()
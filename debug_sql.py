#!/usr/bin/env python3
"""
Debug SQL execution to find the exact issue
"""

import sys
import psycopg2
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings

def debug_sql_execution():
    """Debug SQL execution step by step"""
    
    # Parse database URL
    database_url = settings.DATABASE_URL
    # Format: postgresql://user:password@host:port/database
    parts = database_url.replace('postgresql://', '').split('@')
    user_pass = parts[0].split(':')
    host_port_db = parts[1].split('/')
    host_port = host_port_db[0].split(':')
    
    conn_params = {
        'host': host_port[0],
        'port': int(host_port[1]) if len(host_port) > 1 else 5432,
        'user': user_pass[0],
        'password': user_pass[1],
        'database': host_port_db[1]
    }
    
    print(f"🔧 Connecting to: {conn_params['host']}:{conn_params['port']}/{conn_params['database']}")
    
    try:
        # Connect to database
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        print("✅ Connected successfully")
        
        # Test if users table exists
        print("\n🔍 Checking if users table exists...")
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
        users_exists = cursor.fetchone()[0]
        print(f"Users table exists: {users_exists}")
        
        # Test if clients table exists
        print("\n🔍 Checking if clients table exists...")
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'clients')")
        clients_exists = cursor.fetchone()[0]
        print(f"Clients table exists: {clients_exists}")
        
        if clients_exists:
            # Check clients table structure
            print("\n🔍 Checking clients table structure...")
            cursor.execute("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'clients' 
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            for col in columns:
                print(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")
        
        # Now let's try to create the users table step by step
        print("\n🔧 Creating users table...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    hashed_password VARCHAR(255) NOT NULL,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    company VARCHAR(100),
                    role VARCHAR(20) DEFAULT 'user',
                    language VARCHAR(10) DEFAULT 'en',
                    street_address VARCHAR(255),
                    street_address_2 VARCHAR(255),
                    city VARCHAR(100),
                    state VARCHAR(100),
                    zip_code VARCHAR(20),
                    country VARCHAR(10),
                    vat_id VARCHAR(50),
                    tax_code VARCHAR(50),
                    iban VARCHAR(50),
                    acn VARCHAR(50),
                    abn VARCHAR(50),
                    subscriber_number VARCHAR(50),
                    phone_number VARCHAR(20),
                    fax_number VARCHAR(20),
                    mobile_number VARCHAR(20),
                    web_address VARCHAR(255),
                    is_active BOOLEAN DEFAULT TRUE,
                    is_admin BOOLEAN DEFAULT FALSE,
                    last_login TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Users table created successfully")
        except Exception as e:
            print(f"❌ Failed to create users table: {e}")
            conn.rollback()
        
        # Now let's try to create the clients table
        print("\n🔧 Creating clients table...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    name VARCHAR(255) NOT NULL,
                    surname VARCHAR(255),
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    mobile VARCHAR(20),
                    web VARCHAR(255),
                    fax VARCHAR(20),
                    vat_id VARCHAR(50),
                    tax_code VARCHAR(50),
                    address_1 VARCHAR(255),
                    address_2 VARCHAR(255),
                    city VARCHAR(100),
                    state VARCHAR(100),
                    zip_code VARCHAR(20),
                    country VARCHAR(100),
                    language VARCHAR(10) DEFAULT 'en',
                    notes TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    gender VARCHAR(20),
                    birthdate DATE,
                    abn VARCHAR(50),
                    company VARCHAR(255),
                    website VARCHAR(255),
                    title VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Clients table created successfully")
        except Exception as e:
            print(f"❌ Failed to create clients table: {e}")
            conn.rollback()
        
        # Test if we can now create the index
        print("\n🔧 Creating index on clients(user_id)...")
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_clients_user ON clients(user_id)")
            conn.commit()
            print("✅ Index created successfully")
        except Exception as e:
            print(f"❌ Failed to create index: {e}")
            conn.rollback()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    debug_sql_execution()

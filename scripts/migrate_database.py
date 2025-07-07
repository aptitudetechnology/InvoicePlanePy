"""
Database migration to add missing role column to users table
This fixes the sqlalchemy.exc.ProgrammingError: column users.role does not exist
"""

from sqlalchemy import text
from app.database import engine
import logging

logger = logging.getLogger(__name__)

def migrate_add_role_column():
    """Add role column to users table if it doesn't exist"""
    try:
        with engine.begin() as conn:
            # Check if role column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'role'
            """))
            
            if result.fetchone() is None:
                logger.info("Adding missing 'role' column to users table...")
                
                # Add the role column
                conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'"))
                
                # Update existing users
                conn.execute(text("UPDATE users SET role = 'user' WHERE role IS NULL"))
                conn.execute(text("UPDATE users SET role = 'admin' WHERE username = 'admin' OR is_admin = true"))
                
                logger.info("✅ Successfully added 'role' column to users table")
            else:
                logger.info("✅ 'role' column already exists in users table")
                
    except Exception as e:
        logger.error(f"❌ Error adding 'role' column: {e}")
        raise

def migrate_add_profile_columns():
    """Add missing profile columns to users table"""
    try:
        with engine.begin() as conn:
            # List of columns to add
            columns_to_add = [
                ("company", "VARCHAR(100)"),
                ("language", "VARCHAR(10) DEFAULT 'en'"),
                ("street_address", "VARCHAR(255)"),
                ("street_address_2", "VARCHAR(255)"),
                ("city", "VARCHAR(100)"),
                ("state", "VARCHAR(100)"),
                ("zip_code", "VARCHAR(20)"),
                ("country", "VARCHAR(10)"),
                ("vat_id", "VARCHAR(50)"),
                ("tax_code", "VARCHAR(50)"),
                ("iban", "VARCHAR(50)"),
                ("acn", "VARCHAR(50)"),
                ("abn", "VARCHAR(50)"),
                ("subscriber_number", "VARCHAR(50)"),
                ("phone_number", "VARCHAR(20)"),
                ("fax_number", "VARCHAR(20)"),
                ("mobile_number", "VARCHAR(20)"),
                ("web_address", "VARCHAR(255)"),
                ("last_login", "TIMESTAMP")
            ]
            
            for column_name, column_type in columns_to_add:
                # Check if column exists
                result = conn.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = '{column_name}'
                """))
                
                if result.fetchone() is None:
                    logger.info(f"Adding missing '{column_name}' column to users table...")
                    conn.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"))
                    logger.info(f"✅ Successfully added '{column_name}' column")
                else:
                    logger.info(f"✅ '{column_name}' column already exists")
                    
    except Exception as e:
        logger.error(f"❌ Error adding profile columns: {e}")
        raise

def migrate_create_api_keys_table():
    """Create the api_keys table if it doesn't exist"""
    try:
        with engine.begin() as conn:
            # Check if api_keys table exists
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'api_keys'
            """))
            
            if result.fetchone() is None:
                logger.info("Creating api_keys table...")
                
                # Create the api_keys table
                conn.execute(text("""
                    CREATE TABLE api_keys (
                        id SERIAL PRIMARY KEY,
                        key_hash VARCHAR(255) UNIQUE NOT NULL,
                        key_prefix VARCHAR(10) NOT NULL,
                        name VARCHAR(100),
                        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        is_active BOOLEAN DEFAULT true,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        last_used_at TIMESTAMP WITH TIME ZONE,
                        expires_at TIMESTAMP WITH TIME ZONE
                    )
                """))
                
                # Create indexes
                conn.execute(text("CREATE INDEX idx_api_keys_key_hash ON api_keys(key_hash)"))
                conn.execute(text("CREATE INDEX idx_api_keys_user_id ON api_keys(user_id)"))
                
                logger.info("✅ Successfully created api_keys table")
            else:
                logger.info("✅ api_keys table already exists")
                
    except Exception as e:
        logger.error(f"❌ Error creating api_keys table: {e}")
        raise

def migrate_update_clients_table():
    """Add missing columns to clients table"""
    try:
        with engine.begin() as conn:
            # List of columns to add to clients table
            columns_to_add = [
                ("gender", "VARCHAR(20)"),
                ("birthdate", "DATE"),
                ("abn", "VARCHAR(50)"),  # Australian Business Number
                ("language", "VARCHAR(10) DEFAULT 'en'"),
                ("is_active", "BOOLEAN DEFAULT true")
            ]
            
            for column_name, column_type in columns_to_add:
                # Check if column exists
                result = conn.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'clients' AND column_name = '{column_name}'
                """))
                
                if result.fetchone() is None:
                    logger.info(f"Adding missing '{column_name}' column to clients table...")
                    conn.execute(text(f"ALTER TABLE clients ADD COLUMN {column_name} {column_type}"))
                    logger.info(f"✅ Successfully added '{column_name}' column to clients table")
                else:
                    logger.info(f"✅ '{column_name}' column already exists in clients table")
                    
            # Update column types for existing columns to match new requirements
            column_updates = [
                ("address_1", "VARCHAR(255)"),  # Increase from 100
                ("address_2", "VARCHAR(255)"),  # Increase from 100
                ("city", "VARCHAR(100)"),       # Increase from 45
                ("state", "VARCHAR(100)"),      # Increase from 35
                ("zip_code", "VARCHAR(20)"),    # Increase from 15
                ("country", "VARCHAR(50)"),     # Increase from 35
                ("website", "VARCHAR(255)")     # Increase from 100
            ]
            
            for column_name, new_type in column_updates:
                try:
                    logger.info(f"Updating '{column_name}' column type in clients table...")
                    conn.execute(text(f"ALTER TABLE clients ALTER COLUMN {column_name} TYPE {new_type}"))
                    logger.info(f"✅ Successfully updated '{column_name}' column type")
                except Exception as e:
                    logger.warning(f"⚠️  Could not update '{column_name}' column type: {e}")
                    
    except Exception as e:
        logger.error(f"❌ Error updating clients table: {e}")
        raise

def migrate_create_product_tables():
    """Create product families and units tables if they don't exist"""
    try:
        with engine.begin() as conn:
            # Check if product_families table exists
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'product_families'
            """))
            
            if result.fetchone() is None:
                logger.info("Creating product_families table...")
                
                conn.execute(text("""
                    CREATE TABLE product_families (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        description TEXT,
                        is_active BOOLEAN DEFAULT true,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                logger.info("✅ Successfully created product_families table")
            else:
                logger.info("✅ product_families table already exists")

            # Check if product_units table exists
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'product_units'
            """))
            
            if result.fetchone() is None:
                logger.info("Creating product_units table...")
                
                conn.execute(text("""
                    CREATE TABLE product_units (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        abbreviation VARCHAR(10) NOT NULL,
                        description TEXT,
                        is_active BOOLEAN DEFAULT true,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                logger.info("✅ Successfully created product_units table")
            else:
                logger.info("✅ product_units table already exists")
                
            # Add foreign key columns to products table if they don't exist
            columns_to_add = [
                ("family_id", "INTEGER REFERENCES product_families(id)"),
                ("unit_id", "INTEGER REFERENCES product_units(id)")
            ]
            
            for column_name, column_type in columns_to_add:
                # Check if column exists
                result = conn.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'products' AND column_name = '{column_name}'
                """))
                
                if result.fetchone() is None:
                    logger.info(f"Adding '{column_name}' column to products table...")
                    conn.execute(text(f"ALTER TABLE products ADD COLUMN {column_name} {column_type}"))
                    logger.info(f"✅ Successfully added '{column_name}' column to products table")
                else:
                    logger.info(f"✅ '{column_name}' column already exists in products table")
                    
    except Exception as e:
        logger.error(f"❌ Error creating product tables: {e}")
        raise

def run_migrations():
    """Run all database migrations"""
    logger.info("🔄 Running database migrations...")
    
    try:
        migrate_add_role_column()
        migrate_add_profile_columns()
        migrate_create_api_keys_table()
        migrate_update_clients_table()
        migrate_create_product_tables()
        logger.info("✅ All database migrations completed successfully")
    except Exception as e:
        logger.error(f"❌ Database migration failed: {e}")
        raise

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Run migrations
    run_migrations()

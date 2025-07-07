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

def run_migrations():
    """Run all database migrations"""
    logger.info("🔄 Running database migrations...")
    
    try:
        migrate_add_role_column()
        migrate_add_profile_columns()
        logger.info("✅ All database migrations completed successfully")
    except Exception as e:
        logger.error(f"❌ Database migration failed: {e}")
        raise

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Run migrations
    run_migrations()

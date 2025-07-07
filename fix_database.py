#!/usr/bin/env python3
"""
Fix missing role column in users table
This script fixes the sqlalchemy.exc.ProgrammingError: column users.role does not exist
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def fix_database():
    """Fix the database by adding missing columns"""
    print("🔧 Fixing InvoicePlane Python database...")
    print("=" * 50)
    
    try:
        # Import and run the migration
        from scripts.migrate_database import run_migrations
        run_migrations()
        print("=" * 50)
        print("✅ Database fix completed successfully!")
        print("🚀 You can now log in to the application.")
        return True
        
    except Exception as e:
        print(f"❌ Database fix failed: {e}")
        print("\nManual fix instructions:")
        print("Connect to your PostgreSQL database and run:")
        print("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user';")
        print("UPDATE users SET role = 'user' WHERE role IS NULL;")
        print("UPDATE users SET role = 'admin' WHERE username = 'admin' OR is_admin = true;")
        return False

if __name__ == "__main__":
    success = fix_database()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Script to delete all products from the database.
Use this before re-importing data with the fixed import script.
"""
import sys
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete
from sqlalchemy.exc import SQLAlchemyError

# Import the app settings
sys.path.append('.')
try:
    from app.config import settings
    from app.models.product import Product
    from app.database import Base
except ImportError as e:
    print(f"❌ Failed to import required modules: {e}")
    print("Make sure you're running this from the InvoicePlanePy root directory")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_session():
    """Create and return a new database session."""
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

def delete_all_products(dry_run=False):
    """
    Delete all products from the database.

    Args:
        dry_run: If True, only show what would be deleted without actually deleting
    """
    session = get_session()

    try:
        # Count what we're about to delete
        product_count = session.query(Product).count()

        print(f"📊 Found {product_count} products")

        if product_count == 0:
            print("✅ No products to delete")
            return True

        # Confirm deletion
        if not dry_run:
            confirm = input(f"⚠️  This will permanently delete {product_count} products. Continue? (yes/no): ")
            if confirm.lower() not in ['yes', 'y']:
                print("❌ Deletion cancelled")
                return False

        if dry_run:
            print("🔍 DRY RUN: Would delete the following:")
            print(f"   - {product_count} products")
            return True

        # Delete products
        print("🗑️  Deleting products...")
        deleted_products = session.execute(delete(Product)).rowcount
        print(f"   ✅ Deleted {deleted_products} products")

        # Commit the changes
        session.commit()
        print("✅ All deletions committed successfully")

        return True

    except SQLAlchemyError as e:
        logger.error(f"Database error during deletion: {e}")
        session.rollback()
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during deletion: {e}")
        session.rollback()
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        session.close()

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        print("🔍 Running in DRY RUN mode (no actual deletions)")
        success = delete_all_products(dry_run=True)
    else:
        print("🗑️  Running in DELETE mode (will actually delete data)")
        success = delete_all_products(dry_run=False)

    if success:
        print("\n🎉 Operation completed successfully!")
        if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
            print("💡 To actually delete the data, run without --dry-run flag")
        else:
            print("💡 You can now re-run the import script to import fresh data")
    else:
        print("\n❌ Operation failed!")
        sys.exit(1)

if __name__ == "__main__":
    print("🧹 InvoicePlanePy Product Deletion Script")
    print("=" * 50)
    main()
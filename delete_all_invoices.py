#!/usr/bin/env python3
"""
Script to delete all invoices and invoice items from the database.
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
    from app.models.invoice import Invoice, InvoiceItem
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

def delete_all_invoices(dry_run=False):
    """
    Delete all invoices and invoice items from the database.

    Args:
        dry_run: If True, only show what would be deleted without actually deleting
    """
    session = get_session()

    try:
        # Count what we're about to delete
        invoice_count = session.query(Invoice).count()
        item_count = session.query(InvoiceItem).count()

        print(f"📊 Found {invoice_count} invoices and {item_count} invoice items")

        if invoice_count == 0 and item_count == 0:
            print("✅ No invoices or items to delete")
            return True

        # Confirm deletion
        if not dry_run:
            confirm = input(f"⚠️  This will permanently delete {invoice_count} invoices and {item_count} items. Continue? (yes/no): ")
            if confirm.lower() not in ['yes', 'y']:
                print("❌ Deletion cancelled")
                return False

        if dry_run:
            print("🔍 DRY RUN: Would delete the following:")
            print(f"   - {invoice_count} invoices")
            print(f"   - {item_count} invoice items")
            return True

        # Delete in correct order (items first due to foreign keys)
        print("🗑️  Deleting invoice items...")
        deleted_items = session.execute(delete(InvoiceItem)).rowcount
        print(f"   ✅ Deleted {deleted_items} invoice items")

        print("🗑️  Deleting invoices...")
        deleted_invoices = session.execute(delete(Invoice)).rowcount
        print(f"   ✅ Deleted {deleted_invoices} invoices")

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
        success = delete_all_invoices(dry_run=True)
    else:
        print("🗑️  Running in DELETE mode (will actually delete data)")
        success = delete_all_invoices(dry_run=False)

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
    print("🧹 InvoicePlanePy Invoice Deletion Script")
    print("=" * 50)
    main()
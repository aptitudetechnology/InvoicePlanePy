#!/usr/bin/env python3
"""
Script to delete all clients from the database.
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
    from app.models.quotes import Quote, QuoteItem
    from app.models.client import Client
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

def delete_all_clients(dry_run=False):
    """
    Delete all clients from the database.

    Args:
        dry_run: If True, only show what would be deleted without actually deleting
    """
    session = get_session()

    try:
        # Count what we're about to delete
        client_count = session.query(Client).count()
        quote_count = session.query(Quote).count()
        quote_item_count = session.query(QuoteItem).count()

        print(f"📊 Found {client_count} clients, {quote_count} quotes, {quote_item_count} quote items")

        if client_count == 0 and quote_count == 0:
            print("✅ No clients or quotes to delete")
            return True

        # Confirm deletion
        if not dry_run:
            confirm = input(f"⚠️  This will permanently delete {quote_count} quotes, {quote_item_count} quote items, and {client_count} clients. Continue? (yes/no): ")
            if confirm.lower() not in ['yes', 'y']:
                print("❌ Deletion cancelled")
                return False

        if dry_run:
            print("🔍 DRY RUN: Would delete the following:")
            print(f"   - {quote_count} quotes")
            print(f"   - {quote_item_count} quote items")
            print(f"   - {client_count} clients")
            return True

        # Delete quotes and quote items first (due to foreign key constraints)
        print("🗑️  Deleting quotes and quote items...")
        deleted_quote_items = session.execute(delete(QuoteItem)).rowcount
        deleted_quotes = session.execute(delete(Quote)).rowcount
        print(f"   ✅ Deleted {deleted_quote_items} quote items")
        print(f"   ✅ Deleted {deleted_quotes} quotes")

        # Delete clients
        print("🗑️  Deleting clients...")
        deleted_clients = session.execute(delete(Client)).rowcount
        print(f"   ✅ Deleted {deleted_clients} clients")

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
        success = delete_all_clients(dry_run=True)
    else:
        print("🗑️  Running in DELETE mode (will actually delete data)")
        success = delete_all_clients(dry_run=False)

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
    print("🧹 InvoicePlanePy Client Deletion Script")
    print("=" * 50)
    main()
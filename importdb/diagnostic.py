#!/usr/bin/env python3
"""
Diagnostic script to check import results and debug issues
Run this from inside the Docker container to see detailed import verification
"""
import sys
import os
sys.path.append('/app')

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

from app.config import settings
from sqlalchemy import create_engine
from app.models.invoice import Invoice, InvoiceItem
from app.models.tax_rate import TaxRate
from sqlalchemy.orm import sessionmaker, joinedload

def check_database_content():
    """Check what data is actually in the database"""
    print("\n" + "="*60)
    print("DATABASE CONTENT CHECK")
    print("="*60)

    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Count records
        invoice_count = session.query(Invoice).count()
        item_count = session.query(InvoiceItem).count()
        tax_rate_count = session.query(TaxRate).count()

        print(f"Database contains:")
        print(f"  - {invoice_count} invoices")
        print(f"  - {item_count} invoice items")
        print(f"  - {tax_rate_count} tax rates")

        if invoice_count == 0:
            print("\n❌ No invoices found! Import may have failed.")
            return

        # Check first few invoices
        invoices = session.query(Invoice).options(joinedload(Invoice.items)).limit(3).all()

        for i, inv in enumerate(invoices, 1):
            print(f"\n📄 Invoice {i}: {inv.invoice_number} (ID: {inv.id})")
            print(f"   Status: {inv.status}")
            print(f"   Dates: Issue={inv.issue_date}, Due={inv.due_date}")
            print(f"   Client ID: {inv.client_id}, User ID: {inv.user_id}")
            print(f"   Invoice totals: Subtotal={inv.subtotal}, Tax={inv.tax_total}, Total={inv.total}, Balance={inv.balance}")

            if inv.items:
                print(f"   ✅ Has {len(inv.items)} items")
                for j, item in enumerate(inv.items[:2], 1):  # Show first 2 items
                    status = "✅" if item.name and item.quantity and item.price else "❌"
                    print(f"     {status} Item {j}: \"{item.name}\" (Qty: {item.quantity}, Price: {item.price})")
                    print(f"         Description: \"{item.description}\"")
                    print(f"         Totals: Subtotal={item.subtotal}, Tax={item.tax_amount}, Total={item.total}")
            else:
                print("   ❌ No items found!")

    except Exception as e:
        print(f"❌ Error during database check: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

def run_verification():
    """Run the same verification as the web interface"""
    print("\n" + "="*60)
    print("IMPORT VERIFICATION")
    print("="*60)

    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        invoices = session.query(Invoice).options(joinedload(Invoice.items)).all()

        verification = {
            "total_invoices": len(invoices),
            "invoices_with_items": 0,
            "invoices_with_totals": 0,
            "issues": [],
            "sample_invoices": []
        }

        print(f"Checking {len(invoices)} invoices...")

        for invoice in invoices[:5]:  # Check first 5 as samples
            has_items = len(invoice.items) > 0
            has_totals = all([
                invoice.subtotal is not None,
                invoice.total is not None,
                invoice.balance is not None
            ])

            if has_items:
                verification["invoices_with_items"] += 1
            if has_totals:
                verification["invoices_with_totals"] += 1

            # Check items
            for item in invoice.items:
                if not item.name or item.name.strip() == "":
                    verification["issues"].append(f"Invoice {invoice.invoice_number}: Item missing name")
                if item.quantity is None:
                    verification["issues"].append(f"Invoice {invoice.invoice_number}: Item missing quantity")
                if item.price is None:
                    verification["issues"].append(f"Invoice {invoice.invoice_number}: Item missing price")

        # Results
        print("\n📊 VERIFICATION RESULTS:")
        print(f"   Total invoices: {verification['total_invoices']}")
        print(f"   Invoices with items: {verification['invoices_with_items']}")
        print(f"   Invoices with totals: {verification['invoices_with_totals']}")
        print(f"   Issues found: {len(verification['issues'])}")

        if verification['issues']:
            print("\n⚠️  ISSUES FOUND:")
            for issue in verification['issues'][:10]:
                print(f"   - {issue}")
            if len(verification['issues']) > 10:
                print(f"   ... and {len(verification['issues']) - 10} more issues")

        # Overall assessment
        if verification['total_invoices'] == 0:
            print("\n❌ STATUS: No invoices found")
        elif len(verification['issues']) == 0 and verification['invoices_with_items'] == verification['total_invoices']:
            print("\n✅ STATUS: Import successful - all data verified!")
        else:
            print(f"\n⚠️  STATUS: Issues found - {len(verification['issues'])} problems detected")

    except Exception as e:
        print(f"❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

def test_sql_parsing():
    """Test parsing the SQL file to see what data is available"""
    print("\n" + "="*60)
    print("SQL FILE PARSING TEST")
    print("="*60)

    from importdb.import_legacy_data import parse_inserts, list_tables

    sql_file = '/app/importdb/invoiceplane.sql'

    if not os.path.exists(sql_file):
        print(f"❌ SQL file not found: {sql_file}")
        return

    try:
        print(f"📁 Checking SQL file: {sql_file}")

        tables = list_tables(sql_file)
        print(f"📋 Tables found: {tables}")

        if 'ip_invoices' in tables:
            invoices = list(parse_inserts(sql_file, 'ip_invoices'))
            print(f"📄 Invoice records: {len(invoices)}")

            if invoices:
                print("🔍 Sample invoice fields:")
                sample = invoices[0]
                for key in sorted(sample.keys())[:15]:  # Show first 15 fields alphabetically
                    value = sample[key]
                    if len(str(value)) > 50:
                        value = str(value)[:47] + "..."
                    print(f"   {key}: {value}")

        if 'ip_invoice_items' in tables:
            items = list(parse_inserts(sql_file, 'ip_invoice_items'))
            print(f"📦 Invoice item records: {len(items)}")

            if items:
                print("🔍 Sample item fields:")
                sample = items[0]
                for key in sorted(sample.keys())[:15]:  # Show first 15 fields alphabetically
                    value = sample[key]
                    if len(str(value)) > 50:
                        value = str(value)[:47] + "..."
                    print(f"   {key}: {value}")

    except Exception as e:
        print(f"❌ Error parsing SQL file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 InvoicePlane Import Diagnostic Tool")
    print("=====================================")

    try:
        test_sql_parsing()
        check_database_content()
        run_verification()

        print("\n" + "="*60)
        print("✅ DIAGNOSTIC COMPLETE")
        print("="*60)
        print("\nIf you see issues above, the import script may need fixes.")
        print("Check the field mappings in importdb/import_legacy_data.py")

    except Exception as e:
        print(f"\n❌ DIAGNOSTIC FAILED: {e}")
        import traceback
        traceback.print_exc()
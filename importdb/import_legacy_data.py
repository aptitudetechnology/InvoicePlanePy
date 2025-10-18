#!/usr/bin/env python3
"""
Interactive InvoicePlane PHP SQL Importer

Allows you to select which legacy table to import into the Python version.
Supports mapping legacy fields to new SQLAlchemy models.
"""
import os
import re
import sys
import logging
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
from app.models.client import Client
from app.models.product import Product
from app.models.invoice import Invoice, InvoiceItem
# TODO: Import other models as needed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SQL_FILE = os.path.join(os.path.dirname(__file__), "invoiceplane.sql")
TABLE_MAP = {
    "ip_clients": "clients",
    # Add more mappings as you add support
}

FIELD_MAP_CLIENTS = {
    # Legacy field : New model field
    "client_name": "name",
    "client_surname": "surname",
    "client_language": "language",
    "client_address_1": "address_1",
    "client_address_2": "address_2",
    "client_city": "city",
    "client_state": "state",
    "client_zip": "zip_code",
    "client_country": "country",
    "client_phone": "phone",
    "client_fax": "fax",
    "client_mobile": "mobile",
    "client_email": "email",
    "client_web": "website",
    "client_gender": "gender",
    "client_birthdate": "birthdate",
    "client_company": "company",
    "client_active": "is_active",
    # Add more as needed
}

FIELD_MAP_PRODUCTS = {
    # Legacy field : New model field
    "product_name": "name",
    "product_description": "description",
    "product_price": "price",
    "product_sku": "sku",
    "product_tax_rate": "tax_rate",
    # Add more as needed
}

FIELD_MAP_INVOICES = {
    # Legacy field : New model field
    "invoice_number": "invoice_number",
    "invoice_date_created": "issue_date",
    "invoice_date_due": "due_date",
    "invoice_terms": "terms",
    "invoice_status_id": "status",
    "user_id": "user_id",
    "client_id": "client_id",
    # Add more as needed
}

FIELD_MAP_INVOICE_ITEMS = {
    # Legacy field : New model field
    "item_name": "name",
    "item_description": "description",
    "item_quantity": "quantity",
    "item_price": "price",
    "item_order": "order",
    # Add more as needed
}

def get_session():
    """Create and return a new database session."""
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

def parse_date(date_str):
    """Parse date string from legacy format."""
    if not date_str or date_str == '0000-00-00':
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        logger.warning(f"Invalid date format: {date_str}")
        return None

def parse_gender(gender_int):
    """Convert legacy gender int to string."""
    if gender_int == '0':
        return 'male'
    elif gender_int == '1':
        return 'female'
    else:
        return None

def list_tables(sql_file):
    """Return a list of legacy tables found in the SQL file."""
    tables = set()
    try:
        with open(sql_file, "r", encoding='utf-8') as f:
            for line in f:
                m = re.match(r"CREATE TABLE `([a-zA-Z0-9_]+)`", line)
                if m:
                    tables.add(m.group(1))
    except FileNotFoundError:
        logger.error(f"SQL file not found: {sql_file}")
        return []
    return sorted(list(tables))

def parse_inserts(sql_file, table):
    """Yield each INSERT statement for the given table."""
    pattern = re.compile(rf"INSERT INTO `{table}` \((.*?)\) VALUES(.*?);", re.DOTALL)
    try:
        with open(sql_file, "r", encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        logger.error(f"SQL file not found: {sql_file}")
        return

    for match in pattern.finditer(content):
        fields = [f.strip('` ') for f in match.group(1).split(',')]
        values_blob = match.group(2)
        # Split values tuples - handle escaped quotes properly
        tuples = re.findall(r"\((.*?)\)", values_blob, re.DOTALL)
        for tup in tuples:
            # Split on commas but respect quoted strings
            vals = []
            current_val = ""
            in_quotes = False
            for char in tup:
                if char == "'" and not in_quotes:
                    in_quotes = True
                elif char == "'" and in_quotes:
                    in_quotes = False
                elif char == "," and not in_quotes:
                    vals.append(current_val.strip())
                    current_val = ""
                    continue
                current_val += char
            vals.append(current_val.strip())

            # Clean up quotes
            vals = [v.strip("'") for v in vals]
            yield dict(zip(fields, vals))

def import_clients(dry_run=False, sql_file=None):
    """Import clients from legacy ip_clients table."""
    if sql_file is None:
        sql_file = SQL_FILE
    session = get_session()
    imported = 0
    skipped = 0

    try:
        logger.info("Starting client import...")
        rows = list(parse_inserts(sql_file, "ip_clients"))
        total = len(rows)
        logger.info(f"Found {total} client records to import")

        for i, row in enumerate(rows):
            if (i + 1) % 10 == 0:
                logger.info(f"Processing record {i+1}/{total}")

            # Map fields
            mapped = {}
            for legacy_field, new_field in FIELD_MAP_CLIENTS.items():
                if legacy_field in row:
                    value = row[legacy_field]
                    if value == 'NULL' or value == '':
                        mapped[new_field] = None
                    else:
                        mapped[new_field] = value

            # Type conversions
            if 'client_active' in row:
                mapped["is_active"] = bool(int(row.get("client_active", 1)))

            if 'client_birthdate' in row:
                mapped["birthdate"] = parse_date(row["client_birthdate"])

            if 'client_gender' in row:
                mapped["gender"] = parse_gender(row["client_gender"])

            # Create client object
            try:
                client = Client(**mapped)
                if not dry_run:
                    session.add(client)
                imported += 1
            except Exception as e:
                logger.error(f"Error creating client from row {row}: {e}")
                skipped += 1
                continue

        if not dry_run:
            session.commit()
            logger.info(f"Successfully imported {imported} clients")
        else:
            logger.info(f"Dry run: Would import {imported} clients")

        if skipped > 0:
            logger.warning(f"Skipped {skipped} records due to errors")

    except SQLAlchemyError as e:
        logger.error(f"Database error during import: {e}")
        session.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error during import: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def import_products(dry_run=False, sql_file=None):
    """Import products from legacy ip_products table."""
    if sql_file is None:
        sql_file = SQL_FILE
    session = get_session()
    imported = 0
    skipped = 0

    try:
        logger.info("Starting product import...")
        rows = list(parse_inserts(sql_file, "ip_products"))
        total = len(rows)
        logger.info(f"Found {total} product records to import")

        for i, row in enumerate(rows):
            if (i + 1) % 10 == 0:
                logger.info(f"Processing record {i+1}/{total}")

            # Map fields
            mapped = {}
            for legacy_field, new_field in FIELD_MAP_PRODUCTS.items():
                if legacy_field in row:
                    value = row[legacy_field]
                    if value == 'NULL' or value == '':
                        mapped[new_field] = None
                    else:
                        mapped[new_field] = value

            # Type conversions
            if 'product_price' in row and row['product_price'] not in ['NULL', '']:
                try:
                    mapped["price"] = float(row["product_price"])
                except ValueError:
                    mapped["price"] = 0.00

            if 'product_tax_rate' in row and row['product_tax_rate'] not in ['NULL', '']:
                try:
                    mapped["tax_rate"] = float(row["product_tax_rate"])
                except ValueError:
                    mapped["tax_rate"] = 0.00

            # Create product object
            try:
                product = Product(**mapped)
                if not dry_run:
                    session.add(product)
                imported += 1
            except Exception as e:
                logger.error(f"Error creating product from row {row}: {e}")
                skipped += 1
                continue

        if not dry_run:
            session.commit()
            logger.info(f"Successfully imported {imported} products")
        else:
            logger.info(f"Dry run: Would import {imported} products")

        if skipped > 0:
            logger.warning(f"Skipped {skipped} records due to errors")

    except SQLAlchemyError as e:
        logger.error(f"Database error during import: {e}")
        session.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error during import: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def import_invoices(dry_run=False, sql_file=None):
    """Import invoices from legacy ip_invoices and ip_invoice_items tables."""
    if sql_file is None:
        sql_file = SQL_FILE
    session = get_session()
    imported = 0
    skipped = 0

    try:
        logger.info("Starting invoice import...")
        rows = list(parse_inserts(sql_file, "ip_invoices"))
        total = len(rows)
        logger.info(f"Found {total} invoice records to import")

        for i, row in enumerate(rows):
            if (i + 1) % 10 == 0:
                logger.info(f"Processing record {i+1}/{total}")

            # Map fields
            mapped = {}
            for legacy_field, new_field in FIELD_MAP_INVOICES.items():
                if legacy_field in row:
                    value = row[legacy_field]
                    if value == 'NULL' or value == '':
                        mapped[new_field] = None
                    else:
                        mapped[new_field] = value

            # Type conversions
            if 'invoice_date_created' in row:
                mapped["issue_date"] = parse_date(row["invoice_date_created"])

            if 'invoice_date_due' in row:
                mapped["due_date"] = parse_date(row["invoice_date_due"])

            # Create invoice object
            try:
                invoice = Invoice(**mapped)
                if not dry_run:
                    session.add(invoice)
                    session.flush()  # Get invoice ID for items

                    # Import invoice items
                    invoice_id = row.get("invoice_id")
                    if invoice_id:
                        item_rows = list(parse_inserts(sql_file, "ip_invoice_items"))
                        for item_row in item_rows:
                            if item_row.get("invoice_id") == invoice_id:
                                item_mapped = {}
                                for legacy_field, new_field in FIELD_MAP_INVOICE_ITEMS.items():
                                    if legacy_field in item_row:
                                        value = item_row[legacy_field]
                                        if value == 'NULL' or value == '':
                                            item_mapped[new_field] = None
                                        else:
                                            item_mapped[new_field] = value

                                item_mapped["invoice_id"] = invoice.id

                                # Type conversions for items
                                if 'item_quantity' in item_row and item_row['item_quantity'] not in ['NULL', '']:
                                    try:
                                        item_mapped["quantity"] = float(item_row["item_quantity"])
                                    except ValueError:
                                        item_mapped["quantity"] = 1.0

                                if 'item_price' in item_row and item_row['item_price'] not in ['NULL', '']:
                                    try:
                                        item_mapped["price"] = float(item_row["item_price"])
                                    except ValueError:
                                        item_mapped["price"] = 0.00

                                try:
                                    invoice_item = InvoiceItem(**item_mapped)
                                    session.add(invoice_item)
                                except Exception as e:
                                    logger.error(f"Error creating invoice item: {e}")
                                    continue

                imported += 1
            except Exception as e:
                logger.error(f"Error creating invoice from row {row}: {e}")
                skipped += 1
                continue

        if not dry_run:
            session.commit()
            logger.info(f"Successfully imported {imported} invoices")
        else:
            logger.info(f"Dry run: Would import {imported} invoices")

        if skipped > 0:
            logger.warning(f"Skipped {skipped} records due to errors")

    except SQLAlchemyError as e:
        logger.error(f"Database error during import: {e}")
        session.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error during import: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        dry_run = True
        logger.info("Running in DRY RUN mode - no data will be imported")
    else:
        dry_run = False

    tables = list_tables(SQL_FILE)
    if not tables:
        logger.error("No tables found in SQL file")
        return

    print("Legacy tables found:")
    for idx, t in enumerate(tables):
        print(f"  [{idx+1}] {t}")

    while True:
        choice = input("Select a table to import (number) or 'q' to quit: ").strip()
        if choice.lower() == 'q':
            break

        try:
            idx = int(choice) - 1
            table = tables[idx]
        except (ValueError, IndexError):
            print("Invalid selection. Please enter a valid number.")
            continue

        if table == "ip_clients":
            try:
                import_clients(dry_run=dry_run)
                print("Import completed successfully!")
            except Exception as e:
                logger.error(f"Import failed: {e}")
                print("Import failed. Check logs for details.")
        elif table == "ip_products":
            try:
                import_products(dry_run=dry_run)
                print("Import completed successfully!")
            except Exception as e:
                logger.error(f"Import failed: {e}")
                print("Import failed. Check logs for details.")
        elif table == "ip_invoices":
            try:
                import_invoices(dry_run=dry_run)
                print("Import completed successfully!")
            except Exception as e:
                logger.error(f"Import failed: {e}")
                print("Import failed. Check logs for details.")
        else:
            print(f"Import for table '{table}' not implemented yet.")

        another = input("Import another table? (y/n): ").strip().lower()
        if another != 'y':
            break

if __name__ == "__main__":
    main()

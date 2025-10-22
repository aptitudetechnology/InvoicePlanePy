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
from app.models.user import User
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
    "product_provider_name": "provider_name",
    "product_purchase_price": "purchase_price",
    "product_sumex": "sumex",
    "product_tariff": "tariff",
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
    "item_tax_rate_id": "tax_rate_id",
    "item_product_id": "product_id",
    # Note: item_discount_amount doesn't exist in legacy schema
    # Add more as needed
}

def get_session():
    """Create and return a new database session."""
    logger.info("Creating database session...")
    try:
        engine = create_engine(settings.DATABASE_URL)
        logger.info("Database engine created")
        Session = sessionmaker(bind=engine)
        session = Session()
        logger.info("Database session created successfully")
        return session
    except Exception as e:
        logger.error(f"Failed to create database session: {e}")
        raise

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
    except UnicodeDecodeError as e:
        logger.error(f"Encoding error reading SQL file {sql_file}: {e}")
        raise ValueError(f"SQL file encoding error: {e}")
    except Exception as e:
        logger.error(f"Error reading SQL file {sql_file}: {e}")
        raise
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
    except UnicodeDecodeError as e:
        logger.error(f"Encoding error reading SQL file {sql_file}: {e}. Please ensure the file is UTF-8 encoded.")
        raise ValueError(f"SQL file encoding error: {e}")
    except Exception as e:
        logger.error(f"Error reading SQL file {sql_file}: {e}")
        raise

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
    id_mapping = {}  # Map legacy client_id to new client.id

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
                    session.flush()  # Get the new ID immediately
                    legacy_id = row.get("client_id")
                    if legacy_id:
                        id_mapping[legacy_id] = client.id
                        logger.debug(f"Created client mapping: legacy {legacy_id} -> new {client.id}")
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

        logger.info(f"Created {len(id_mapping)} ID mappings for clients")
        return id_mapping

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
    id_mapping = {}  # Map legacy product_id to new product.id

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

            # Type conversions for additional fields
            if 'product_purchase_price' in row and row['product_purchase_price'] not in ['NULL', '']:
                try:
                    mapped["purchase_price"] = float(row["product_purchase_price"])
                except ValueError:
                    mapped["purchase_price"] = None

            if 'product_sumex' in row and row['product_sumex'] not in ['NULL', '']:
                mapped["sumex"] = bool(int(row["product_sumex"]) if row["product_sumex"].isdigit() else 0)

            if 'product_tariff' in row and row['product_tariff'] not in ['NULL', '']:
                try:
                    mapped["tariff"] = float(row["product_tariff"])
                except ValueError:
                    mapped["tariff"] = None

            # Generate unique SKU if missing
            if not mapped.get("sku"):
                import uuid
                # Generate a unique SKU based on product name or use a UUID
                base_name = mapped.get("name", "product").replace(" ", "_").lower()[:20]
                mapped["sku"] = f"{base_name}_{uuid.uuid4().hex[:8]}"

            # Ensure SKU uniqueness by checking existing records
            original_sku = mapped["sku"]
            counter = 1
            while True:
                existing = session.query(Product).filter_by(sku=mapped["sku"]).first()
                if not existing:
                    break
                mapped["sku"] = f"{original_sku}_{counter}"
                counter += 1

            # Skip products without names (required field)
            if not mapped.get("name"):
                logger.warning(f"Skipping product without name: {row}")
                skipped += 1
                continue

            # Create product object
            try:
                product = Product(**mapped)
                if not dry_run:
                    session.add(product)
                    session.flush()  # Get the new ID immediately
                    legacy_id = row.get("product_id")
                    if legacy_id:
                        id_mapping[legacy_id] = product.id
                        logger.debug(f"Created product mapping: legacy {legacy_id} -> new {product.id}")
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

        logger.info(f"Created {len(id_mapping)} ID mappings for products")
        return id_mapping

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

def import_invoices(dry_run=False, sql_file=None, client_id_mapping=None, product_id_mapping=None):
    """Import invoices from legacy ip_invoices and ip_invoice_items tables."""
    logger.info("import_invoices function called")
    logger.info(f"client_id_mapping: {client_id_mapping is not None} ({len(client_id_mapping) if client_id_mapping else 0} entries)")
    logger.info(f"product_id_mapping: {product_id_mapping is not None} ({len(product_id_mapping) if product_id_mapping else 0} entries)")
    if sql_file is None:
        sql_file = SQL_FILE
    logger.info(f"Using SQL file: {sql_file}")
    
    try:
        session = get_session()
        logger.info("Database session created successfully")
    except Exception as e:
        logger.error(f"Failed to create database session: {e}")
        raise
    
    imported = 0
    skipped = 0

    try:
        logger.info("Starting invoice import...")
        logger.info(f"Reading from SQL file: {sql_file}")
        
        # Debug: Show what tables are found
        all_tables = list_tables(sql_file)
        logger.info(f"Tables found in SQL file: {all_tables}")
        
        # Check for required tables
        required_tables = ["ip_invoices", "ip_invoice_items"]
        missing_tables = [table for table in required_tables if table not in all_tables]
        if missing_tables:
            raise ValueError(f"SQL file is missing required tables: {missing_tables}. Found tables: {all_tables}")
        
        try:
            rows = list(parse_inserts(sql_file, "ip_invoices"))
        except Exception as e:
            logger.error(f"Failed to parse invoice data from SQL file: {e}")
            raise ValueError(f"SQL parsing error: {e}")
        
        total = len(rows)
        logger.info(f"Found {total} invoice records to import")
        
        if total == 0:
            logger.warning("No invoice records found! Check if the SQL file contains ip_invoices table data.")
            return

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

            # Skip invoices without required fields
            if not mapped.get("user_id") or not mapped.get("client_id") or not mapped.get("invoice_number"):
                logger.warning(f"Skipping invoice without required user_id, client_id, or invoice_number: {row}")
                skipped += 1
                continue

            # Map client_id using the ID mapping if provided
            client_id = mapped.get("client_id")
            if client_id and client_id_mapping:
                new_client_id = client_id_mapping.get(str(client_id))
                if new_client_id:
                    mapped["client_id"] = new_client_id
                    logger.debug(f"Mapped legacy client_id {client_id} to new client_id {new_client_id}")
                else:
                    logger.warning(f"No mapping found for legacy client_id {client_id}, skipping invoice: {row}")
                    skipped += 1
                    continue
            elif client_id:
                # Fallback: check if the legacy ID exists directly (for backward compatibility)
                existing_client = session.query(Client).filter_by(id=client_id).first()
                if not existing_client:
                    logger.warning(f"Skipping invoice with non-existent client_id {client_id}: {row}")
                    skipped += 1
                    continue

            # Check if referenced user exists
            user_id = mapped.get("user_id")
            if user_id:
                from app.models.user import User
                existing_user = session.query(User).filter_by(id=user_id).first()
                if not existing_user:
                    logger.warning(f"Skipping invoice with non-existent user_id {user_id}: {row}")
                    skipped += 1
                    continue

            # Check if invoice_number is unique
            invoice_number = mapped.get("invoice_number")
            if invoice_number:
                existing_invoice = session.query(Invoice).filter_by(invoice_number=invoice_number).first()
                if existing_invoice:
                    logger.warning(f"Skipping invoice with duplicate invoice_number {invoice_number}: {row}")
                    skipped += 1
                    continue

            # Create invoice object
            try:
                invoice = Invoice(**mapped)
                if not dry_run:
                    session.add(invoice)
                    session.flush()  # Get invoice ID for items

                    # Import invoice items
                    invoice_id = row.get("invoice_id")
                    if invoice_id:
                        logger.info(f"Processing items for invoice {invoice_id}")
                        try:
                            item_rows = list(parse_inserts(sql_file, "ip_invoice_items"))
                        except Exception as e:
                            logger.error(f"Failed to parse invoice items from SQL file: {e}")
                            raise ValueError(f"SQL parsing error for invoice items: {e}")
                        logger.info(f"Found {len(item_rows)} total invoice item records")
                        
                        # Filter items for this invoice
                        invoice_items = [item for item in item_rows if item.get("invoice_id") == invoice_id]
                        logger.info(f"Found {len(invoice_items)} items for invoice {invoice_id}")
                        
                        if invoice_items:
                            logger.info(f"Sample item for invoice {invoice_id}: {invoice_items[0]}")
                        
                        for item_row in invoice_items:
                                logger.debug(f"Processing invoice item: {item_row}")
                                item_mapped = {}
                                for legacy_field, new_field in FIELD_MAP_INVOICE_ITEMS.items():
                                    if legacy_field in item_row:
                                        value = item_row[legacy_field]
                                        logger.debug(f"Mapping {legacy_field}='{value}' to {new_field}")
                                        if value == 'NULL':
                                            # Handle NULL values - set to None for optional fields, empty string for text fields
                                            if new_field in ['description']:
                                                item_mapped[new_field] = ""
                                            else:
                                                item_mapped[new_field] = None
                                        elif value == '':
                                            # Handle empty strings - keep as empty string for text fields
                                            if new_field in ['name', 'description']:
                                                item_mapped[new_field] = ""
                                            else:
                                                item_mapped[new_field] = None
                                        else:
                                            item_mapped[new_field] = value

                                logger.debug(f"Mapped invoice item: {item_mapped}")

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

                                # Skip invoice items without required fields
                                if not item_mapped.get("name") or item_mapped.get("name") == "":
                                    logger.warning(f"Skipping invoice item without required name: {item_row}")
                                    continue
                                
                                if item_mapped.get("quantity") is None:
                                    logger.warning(f"Skipping invoice item without quantity: {item_row}")
                                    continue
                                    
                                if item_mapped.get("price") is None:
                                    logger.warning(f"Skipping invoice item without price: {item_row}")
                                    continue

                                # Map product_id using the ID mapping if provided
                                product_id = item_mapped.get("product_id")
                                if product_id and product_id_mapping:
                                    new_product_id = product_id_mapping.get(str(product_id))
                                    if new_product_id:
                                        item_mapped["product_id"] = new_product_id
                                        logger.debug(f"Mapped legacy product_id {product_id} to new product_id {new_product_id}")
                                    else:
                                        logger.warning(f"No mapping found for legacy product_id {product_id}, skipping invoice item: {item_row}")
                                        continue
                                elif product_id:
                                    # Fallback: check if the legacy ID exists directly (for backward compatibility)
                                    existing_product = session.query(Product).filter_by(id=product_id).first()
                                    if not existing_product:
                                        logger.warning(f"Skipping invoice item with non-existent product_id {product_id}: {item_row}")
                                        continue

                                # Calculate item totals
                                quantity = item_mapped.get("quantity", 0)
                                price = item_mapped.get("price", 0)
                                # No discount_amount in legacy schema, so set to 0
                                discount_amount = 0.0

                                item_mapped["subtotal"] = quantity * price
                                item_mapped["discount_amount"] = discount_amount

                                # Calculate tax amount based on tax_rate_id
                                tax_amount = 0.0
                                tax_rate_id = item_mapped.get("tax_rate_id")
                                if tax_rate_id and str(tax_rate_id) != '0':
                                    try:
                                        from app.models.tax_rate import TaxRate
                                        tax_rate = session.query(TaxRate).filter_by(id=tax_rate_id).first()
                                        if tax_rate:
                                            # Calculate tax on (subtotal - discount)
                                            taxable_amount = item_mapped["subtotal"] - discount_amount
                                            tax_amount = taxable_amount * (tax_rate.rate / 100)
                                    except Exception as e:
                                        logger.warning(f"Error calculating tax for item: {e}")

                                item_mapped["tax_amount"] = tax_amount
                                item_mapped["total"] = item_mapped["subtotal"] - discount_amount + tax_amount

                                try:
                                    invoice_item = InvoiceItem(**item_mapped)
                                    session.add(invoice_item)
                                    logger.debug(f"Successfully created invoice item: {item_mapped}")
                                except Exception as e:
                                    logger.error(f"Error creating invoice item: {e}")
                                    continue

                    # Calculate invoice totals from items
                    session.flush()  # Ensure all items are saved
                    items = session.query(InvoiceItem).filter_by(invoice_id=invoice.id).all()
                    logger.info(f"Created {len(items)} invoice items for invoice {invoice.id}")

                    if items:
                        invoice.subtotal = sum(item.subtotal for item in items)
                        invoice.tax_total = sum(item.tax_amount for item in items)
                        invoice.discount_amount = sum(item.discount_amount for item in items)
                        invoice.total = sum(item.total for item in items)
                        invoice.balance = invoice.total - invoice.paid_amount if invoice.paid_amount else invoice.total
                    else:
                        # No items, set defaults
                        invoice.subtotal = 0
                        invoice.tax_total = 0
                        invoice.discount_amount = 0
                        invoice.total = 0
                        invoice.balance = 0

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

        logger.info("Invoice import completed")

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

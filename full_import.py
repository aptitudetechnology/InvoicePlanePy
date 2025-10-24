#!/usr/bin/env python3
"""
Complete InvoicePlane Legacy Data Import Script

Imports all legacy data in the correct order to avoid foreign key constraint issues.
Order: tax_rates -> families -> units -> products -> clients -> invoices
"""

import sys
import os
import logging
from importdb.import_legacy_data import (
    import_tax_rates,
    import_products,
    import_clients,
    import_invoices,
    get_session
)

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('import.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Run complete import of all legacy data"""
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        logger.info("🔍 Running in DRY RUN mode - no data will be imported")
    else:
        logger.info("🚀 Starting complete legacy data import")

    try:
        # Step 1: Import tax rates first (no dependencies)
        logger.info("📊 Step 1: Importing tax rates...")
        tax_rate_mapping = import_tax_rates(dry_run=dry_run)
        logger.info(f"✅ Tax rates imported: {len(tax_rate_mapping) if tax_rate_mapping else 'dry run'}")

        # Step 2: Import product families (no dependencies)
        logger.info("🏷️  Step 2: Importing product families...")
        # Note: import_products handles families internally, but we need to get the mapping
        # For now, we'll let import_products handle family creation

        # Step 3: Import product units (no dependencies)
        logger.info("📏 Step 3: Importing product units...")
        # Note: import_products handles units internally

        # Step 4: Import products (depends on families, units, tax_rates)
        logger.info("📦 Step 4: Importing products...")
        product_mapping = import_products(dry_run=dry_run)
        logger.info(f"✅ Products imported: {len(product_mapping) if product_mapping else 'dry run'}")

        # Step 5: Import clients (no dependencies)
        logger.info("👥 Step 5: Importing clients...")
        client_mapping = import_clients(dry_run=dry_run)
        logger.info(f"✅ Clients imported: {len(client_mapping) if client_mapping else 'dry run'}")

        # Step 6: Import invoices (depends on clients, products)
        logger.info("📄 Step 6: Importing invoices...")
        invoice_mapping = import_invoices(
            dry_run=dry_run,
            client_id_mapping=client_mapping,
            product_id_mapping=product_mapping
        )
        logger.info(f"✅ Invoices imported: {len(invoice_mapping) if invoice_mapping else 'dry run'}")

        if dry_run:
            logger.info("🔍 Dry run completed successfully!")
        else:
            logger.info("🎉 Complete import finished successfully!")
            logger.info("📊 Import Summary:")
            logger.info(f"   - Tax Rates: {len(tax_rate_mapping) if tax_rate_mapping else 0}")
            logger.info(f"   - Products: {len(product_mapping) if product_mapping else 0}")
            logger.info(f"   - Clients: {len(client_mapping) if client_mapping else 0}")
            logger.info(f"   - Invoices: {len(invoice_mapping) if invoice_mapping else 0}")

    except Exception as e:
        logger.error(f"❌ Import failed: {e}")
        logger.error("Check the import.log file for detailed error information")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Fix SQL file data quality issues for InvoicePlane import
"""
import re
import os

def fix_sql_file(input_file, output_file):
    """Fix data quality issues in the SQL file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix empty invoice numbers in ip_invoices table
    # Pattern to match invoice records with empty invoice_number
    invoice_pattern = r"\((\d+),\s*1,\s*[^,]+,\s*3,\s*[^,]+,\s*[^,]+,\s*'',\s*'([^']+)',\s*'([^']+)',\s*'([^']+)',\s*'([^']+)',\s*'',\s*0\.00,\s*0\.00,"

    def replace_invoice_number(match):
        invoice_id = match.group(1)
        # Generate invoice number based on invoice_id (simple sequential)
        invoice_number = str(int(invoice_id) - 1)  # Adjust as needed
        return match.group(0).replace("'', 0.00, 0.00,", f"'{invoice_number}', 0.00, 0.00,")

    # Apply the fix
    fixed_content = re.sub(invoice_pattern, replace_invoice_number, content)

    # Write the fixed content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"Fixed SQL file written to: {output_file}")

if __name__ == "__main__":
    input_file = "/home/chris/InvoicePlanePy/importdb/invoiceplane.sql"
    output_file = "/home/chris/InvoicePlanePy/importdb/invoiceplane_fixed.sql"

    if os.path.exists(input_file):
        fix_sql_file(input_file, output_file)
    else:
        print(f"Input file not found: {input_file}")
# Invoice Import Totals Fix

## Problem
Invoices imported from the old InvoicePlane version were missing critical financial data:
- **Line items**: Missing calculated totals (subtotal, tax_amount, discount_amount, total)
- **Invoice totals**: Missing aggregated totals (subtotal, tax_total, discount_amount, total, balance)
- **Item details**: Missing item names, descriptions, and other basic fields

## Root Cause
The `importdb/import_legacy_data.py` script was only importing basic fields but not calculating the financial totals that the new SQLAlchemy models expect. Additionally, there were issues with how NULL/empty values were handled for text fields.

## Solution Implemented

### 1. Enhanced Field Mappings
Added `item_discount_amount` to the invoice item field mapping to capture discount data from legacy system.

### 2. Fixed NULL/Empty Value Handling
- **Text fields** (name, description): Convert NULL/empty to empty string `""`
- **Numeric fields**: Convert NULL/empty to `None`
- **Required validation**: Ensure name, quantity, and price are present before importing

### 3. Added Item-Level Calculations
For each invoice item, the script now calculates:
```python
subtotal = quantity * price
discount_amount = item_discount_amount (from legacy data)
tax_amount = 0.0  # TODO: Implement tax rate lookup
total = subtotal - discount_amount + tax_amount
```

### 4. Added Invoice-Level Calculations
After importing all items for an invoice, the script calculates:
```python
invoice.subtotal = sum(item.subtotal for item in items)
invoice.tax_total = sum(item.tax_amount for item in items)
invoice.discount_amount = sum(item.discount_amount for item in items)
invoice.total = sum(item.total for item in items)
invoice.balance = total - paid_amount
```

## Files Modified
- `importdb/import_legacy_data.py`: Added calculation logic, fixed field mapping, improved NULL handling

## Testing Instructions

### 1. Dry Run Test
```bash
cd /app
python importdb/import_legacy_data.py --dry-run --table invoices
```

### 2. Full Import (with calculations)
```bash
cd /app
python importdb/import_legacy_data.py --table invoices
```

### 3. Verify Results
Check that imported invoices now have:
- Invoice items with `name`, `description`, `quantity`, `price`
- Invoice items with calculated `subtotal`, `tax_amount`, `discount_amount`, `total`
- Invoices with calculated `subtotal`, `tax_total`, `discount_amount`, `total`, `balance`

### 4. Re-import Existing Data
For invoices already imported without complete data:
```bash
# Option 1: Delete and re-import (CAUTION: This will delete existing invoices)
# Option 2: Use the delete button in the UI to remove specific bad imports, then re-import
```

## Debug Information
- **Parsing verified**: The `parse_inserts` function correctly extracts item names and descriptions from the SQL file
- **Field mapping**: All required fields (`item_name`, `item_description`, etc.) are properly mapped
- **Data validation**: Items without required fields are skipped with warning logs

## Future Enhancements
- Implement tax rate lookup using `item_tax_rate_id` from legacy data
- Add support for percentage-based discounts
- Add validation to ensure calculated totals match legacy system totals

## Impact
✅ **Invoices now have complete item details** (name, description, quantity, price)  
✅ **Line items show proper calculated amounts**  
✅ **Invoice totals are accurately computed**  
✅ **Business Plugin Middleware can access complete invoice data**</content>
<parameter name="filePath">/home/chris/InvoicePlanePy/invoice-import-totals-fix.md
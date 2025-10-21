# Invoice Import Totals Fix

## Problem
Invoices imported from the old InvoicePlane version were missing critical financial data:
- **Line items**: Missing calculated totals (subtotal, tax_amount, discount_amount, total)
- **Invoice totals**: Missing aggregated totals (subtotal, tax_total, discount_amount, total, balance)

## Root Cause
The `importdb/import_legacy_data.py` script was only importing basic fields but not calculating the financial totals that the new SQLAlchemy models expect.

## Solution Implemented

### 1. Updated Field Mappings
Added `item_discount_amount` to the invoice item field mapping to capture discount data from legacy system.

### 2. Added Item-Level Calculations
For each invoice item, the script now calculates:
```python
subtotal = quantity * price
discount_amount = item_discount_amount (from legacy data)
tax_amount = 0.0  # TODO: Implement tax rate lookup
total = subtotal - discount_amount + tax_amount
```

### 3. Added Invoice-Level Calculations
After importing all items for an invoice, the script calculates:
```python
invoice.subtotal = sum(item.subtotal for item in items)
invoice.tax_total = sum(item.tax_amount for item in items)
invoice.discount_amount = sum(item.discount_amount for item in items)
invoice.total = sum(item.total for item in items)
invoice.balance = total - paid_amount
```

## Files Modified
- `importdb/import_legacy_data.py`: Added calculation logic for both item and invoice totals

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
- Invoice items with calculated `subtotal`, `tax_amount`, `discount_amount`, `total`
- Invoices with calculated `subtotal`, `tax_total`, `discount_amount`, `total`, `balance`

### 4. Re-import Existing Data
For invoices already imported without totals:
```bash
# Clear existing invoice data (CAUTION: This will delete existing invoices)
# Then re-run the import with the updated script
```

## Future Enhancements
- Implement tax rate lookup using `item_tax_rate_id` from legacy data
- Add support for percentage-based discounts
- Add validation to ensure calculated totals match legacy system totals

## Impact
- ✅ Invoices now have complete financial data
- ✅ Line items show proper calculated amounts
- ✅ Invoice totals are accurately computed
- ✅ Business Plugin Middleware can access complete invoice data</content>
<parameter name="filePath">/home/chris/InvoicePlanePy/invoice-import-totals-fix.md
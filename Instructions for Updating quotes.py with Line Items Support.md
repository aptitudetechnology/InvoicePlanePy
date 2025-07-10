# Instructions for Updating quotes.py with Line Items Support

## Overview
The current `quotes.py` file only handles quote header information (client, dates, status, etc.) but lacks support for quote line items. The user is trying to add/edit line items through a web interface that includes item details like quantity, price, discounts, and tax calculations.

## Current State
- Quote header CRUD operations work
- No line item management functionality
- No item-level calculations
- No quote total aggregation from line items
- Template shows item table but backend doesn't support it

## Required Updates

### 1. Database Model Requirements
Ensure you have a `QuoteItem` model with fields:
- `id` (primary key)
- `quote_id` (foreign key to Quote)
- `name` (item name)
- `description` (item description)
- `quantity` (decimal/float)
- `price` (decimal/float)
- `discount` (decimal/float) - item-level discount
- `tax_rate` (decimal/float) - item-level tax rate
- `subtotal` (calculated: quantity * price)
- `discount_amount` (calculated: subtotal * discount / 100)
- `tax_amount` (calculated: (subtotal - discount_amount) * tax_rate / 100)
- `total` (calculated: subtotal - discount_amount + tax_amount)
- `unit` (optional: unit of measurement)
- `created_at`, `updated_at` timestamps

### 2. API Endpoints to Add

#### Line Item Management
```python
# Add these routes to quotes.py:

@router.post("/{quote_id}/items")
async def add_quote_item(quote_id: int, item_data: dict, db: Session, current_user: User)
# - Validate quote ownership
# - Create new QuoteItem
# - Recalculate quote totals
# - Return updated item data

@router.put("/{quote_id}/items/{item_id}")
async def update_quote_item(quote_id: int, item_id: int, item_data: dict, db: Session, current_user: User)
# - Validate quote and item ownership
# - Update QuoteItem
# - Recalculate quote totals
# - Return updated item data

@router.delete("/{quote_id}/items/{item_id}")
async def delete_quote_item(quote_id: int, item_id: int, db: Session, current_user: User)
# - Validate quote and item ownership
# - Delete QuoteItem
# - Recalculate quote totals
# - Return success response

@router.get("/{quote_id}/items")
async def get_quote_items(quote_id: int, db: Session, current_user: User)
# - Return all items for a quote
# - Include calculated totals
```

### 3. Calculation Functions to Add

```python
def calculate_item_totals(item: QuoteItem) -> QuoteItem:
    """Calculate subtotal, discount_amount, tax_amount, and total for an item"""
    # subtotal = quantity * price
    # discount_amount = subtotal * (discount / 100)
    # tax_amount = (subtotal - discount_amount) * (tax_rate / 100)
    # total = subtotal - discount_amount + tax_amount

def calculate_quote_totals(quote: Quote, db: Session) -> Quote:
    """Recalculate quote totals from all line items"""
    # Sum all item totals
    # Update quote.subtotal, quote.tax_amount, quote.discount_amount, quote.total
    # Save to database
```

### 4. Frontend Integration Points

The template likely has JavaScript that makes AJAX calls to:
- Add new items
- Update existing items
- Delete items
- Recalculate totals in real-time

Ensure your API endpoints return JSON responses compatible with the frontend expectations.

### 5. Form Handling Updates

Update existing quote edit/create forms to:
- Include line items data
- Handle item arrays in form submission
- Validate item data
- Process items alongside quote header data

### 6. Database Query Updates

Update existing quote queries to include line items:
```python
# Use joinedload to eager load items
quote = db.query(Quote).options(joinedload(Quote.items)).filter(Quote.id == quote_id).first()
```

### 7. Permission Checks

Ensure all item operations check:
- Quote ownership (user_id matches or user is admin)
- Quote exists and is accessible
- Item belongs to the specified quote

### 8. Error Handling

Add proper error handling for:
- Invalid calculations (divide by zero, negative quantities, etc.)
- Database constraint violations
- Orphaned items
- Quote total mismatches

## Testing Considerations

1. Test item CRUD operations
2. Test calculation accuracy
3. Test quote total aggregation
4. Test permission boundaries
5. Test error scenarios
6. Test frontend integration

## Next Steps

1. Review the current template to understand exact data structure expected
2. Implement the QuoteItem model if not already exists
3. Add the API endpoints listed above
4. Add calculation functions
5. Update existing quote operations to handle items
6. Test with the frontend interface

## Notes
- The user showed a line item with: Item="test", Quantity=1, Price=33, resulting in $33.00 total
- The interface includes item-level discounts and tax rates
- Tax Rate shows "None" dropdown, suggesting multiple tax rate options
- The interface appears to be a dynamic table with add/remove functionality
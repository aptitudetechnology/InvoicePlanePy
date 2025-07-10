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
- `discount` (decimal/float) - item-level discount percentage
- `tax_rate` (decimal/float) - item-level tax rate percentage
- `subtotal` (calculated: quantity * price)
- `discount_amount` (calculated: subtotal * discount / 100)
- `tax_amount` (calculated: (subtotal - discount_amount) * tax_rate / 100)
- `total` (calculated: subtotal - discount_amount + tax_amount)
- `created_at`, `updated_at` timestamps

### 1b. Quote Model Updates
The Quote model needs these additional fields:
- `item_tax` (sum of all item tax amounts)
- `quote_tax` (additional quote-level tax)
- `discount_percentage` (quote-level discount percentage)
- `quote_pdf_password` (optional PDF password)

### 2. Form Processing Update

The edit form submits items as an array structure:
- `items[0][name]`, `items[0][description]`, etc.
- `items[1][name]`, `items[1][description]`, etc.

Update the `edit_quote_post` function to handle this:

```python
@router.post("/{quote_id}/edit")
async def edit_quote_post(
    quote_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get form data
    form_data = await request.form()
    
    # Extract quote header data
    client_id = form_data.get("client_id")
    quote_number = form_data.get("quote_number")
    # ... other quote fields
    
    # Process items array
    items_data = {}
    for key, value in form_data.items():
        if key.startswith('items['):
            # Parse items[0][name] format
            import re
            match = re.match(r'items\[(\d+)\]\[(\w+)\]', key)
            if match:
                index, field = match.groups()
                if index not in items_data:
                    items_data[index] = {}
                items_data[index][field] = value
    
    # Update quote and items
    # ... implementation details
```

### 3. Additional Routes from Template

The template references these routes that need to be added:

```python
@router.get("/{quote_id}/pdf")
async def download_quote_pdf(quote_id: int, db: Session, current_user: User)
# Generate and return PDF of quote

@router.get("/{quote_id}/email")
async def email_quote(quote_id: int, db: Session, current_user: User)
# Send quote via email

@router.get("/{quote_id}/copy")
async def copy_quote_get(quote_id: int, db: Session, current_user: User)
# Create a copy of the quote (alternative to duplicate route)

@router.delete("/{quote_id}/delete")
async def delete_quote_api(quote_id: int, db: Session, current_user: User)
# DELETE endpoint for AJAX deletion (current code uses POST)
```

### 4. Calculation Functions to Add

The template shows complex totals calculation:

```python
def calculate_quote_totals(quote: Quote, items: List[QuoteItem]) -> dict:
    """Calculate all quote totals based on items and quote-level discounts"""
    
    # Calculate item-level totals
    subtotal = sum(item.subtotal for item in items)
    item_tax = sum(item.tax_amount for item in items)
    item_discounts = sum(item.discount_amount for item in items)
    
    # Apply quote-level discount
    quote_discount_amount = 0
    if quote.discount_percentage:
        taxable_amount = subtotal - item_discounts
        quote_discount_amount = taxable_amount * (quote.discount_percentage / 100)
    
    # Calculate final total
    total = subtotal - item_discounts - quote_discount_amount + item_tax + (quote.quote_tax or 0)
    
    return {
        'subtotal': subtotal,
        'item_tax': item_tax,
        'quote_tax': quote.quote_tax or 0,
        'total_discount': item_discounts + quote_discount_amount,
        'total': total
    }

def calculate_item_totals(quantity: float, price: float, discount: float, tax_rate: float) -> dict:
    """Calculate individual item totals"""
    subtotal = quantity * price
    discount_amount = subtotal * (discount / 100)
    taxable_amount = subtotal - discount_amount
    tax_amount = taxable_amount * (tax_rate / 100)
    total = taxable_amount + tax_amount
    
    return {
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'tax_amount': tax_amount,
        'total': total
    }
```

### 5. Template Data Requirements

Update your quote queries to include all needed relationships:

```python
# In edit_quote and view_quote functions:
quote = db.query(Quote).options(
    joinedload(Quote.client),
    joinedload(Quote.items)
).filter(Quote.id == quote_id).first()

# Ensure quote has all required attributes for template:
# - quote.items (list of QuoteItem objects)
# - quote.client (Client object with name, address, email, etc.)
# - quote.subtotal, quote.item_tax, quote.quote_tax, quote.total
# - quote.discount_percentage
# - quote.quote_pdf_password
```

### 6. Form Field Updates

The template expects these form fields in the POST handler:
- `client_id` (hidden field)
- `quote_number`
- `status` 
- `issue_date`
- `valid_until`
- `quote_pdf_password`
- `notes`
- `discount_percentage`
- `items[n][name]`
- `items[n][description]`
- `items[n][quantity]`
- `items[n][price]`
- `items[n][discount]`
- `items[n][tax_rate]`

### 7. Critical Implementation Notes

**Form Processing Strategy:**
- The template uses traditional form submission, NOT AJAX for items
- All items are submitted together with the quote in one POST request
- JavaScript only handles client-side calculations for immediate feedback
- Server must process the entire items array on form submission

**Item Management:**
- Items are added/removed dynamically in the frontend
- Each item gets a unique index: `items[0]`, `items[1]`, etc.
- When items are removed, gaps may appear in indices
- Backend must handle sparse arrays appropriately

**Calculations:**
- Frontend JavaScript handles immediate calculation updates
- Backend must recalculate and validate all totals on save
- Template shows: subtotal, item tax, quote tax, discount, total
- Both item-level and quote-level discounts are supported

**Tax Rates:**
- Template shows dropdown with: None (0%), 10%, 15%
- These should be configurable in your system
- Each item can have different tax rates

**Delete Functionality:**
- Template JavaScript makes DELETE request to `/quotes/{id}/delete`
- Your current code uses POST for deletion
- Add DELETE endpoint or update frontend to use POST

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
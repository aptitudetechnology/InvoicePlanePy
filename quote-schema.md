# Quote Database Schema Analysis & Fix Recommendations

## Template vs Database Schema Analysis

Based on your Jinja2 template, I can see there are additional complexities:

### Template Field Mapping
Your template shows the application layer uses different field names than the database:

| Template Variable | Database Field | Type | Notes |
|------------------|----------------|------|--------|
| `quote.quote_number` | `quote_number` | VARCHAR(20) | ✅ Match |
| `quote.status` | `status` | VARCHAR(20) | ✅ Match |
| `quote.issue_date` | `issue_date` | DATE | ✅ Match |
| `quote.valid_until` | `valid_until` | DATE | ✅ Match |
| `quote.notes` | `notes` | TEXT | ✅ Match |
| `quote.subtotal` | `subtotal` | NUMERIC(10,2) | ✅ Match |
| `quote.tax_total` | `tax_total` | NUMERIC(10,2) | ✅ Match |
| `quote.total` | `total` | NUMERIC(10,2) | ✅ Match |

### Item Fields - Template vs Database Mismatch
The template reveals your items have more fields than the basic database schema:

**Template expects these item fields:**
- `item.name` → Database: `product_name` ✅
- `item.description` → Database: `description` ✅  
- `item.quantity` → Database: `quantity` ✅
- `item.price` → Database: `unit_price` ⚠️ **Name mismatch**
- `item.discount` → **Missing from database schema**
- `item.tax_rate` → **Missing from database schema**
- `item.subtotal` → **Calculated field, not stored**
- `item.discount_amount` → **Calculated field, not stored**
- `item.tax_amount` → **Calculated field, not stored**
- `item.total` → Database: `line_total` ⚠️ **Name mismatch**

### Missing Database Fields for Full Template Support
Your current database schema is missing these fields that the template expects:

```sql
-- Add these columns to quote_items table to support the template
ALTER TABLE quote_items ADD COLUMN discount_percentage NUMERIC(5,2) DEFAULT 0.00;
ALTER TABLE quote_items ADD COLUMN tax_rate NUMERIC(5,2) DEFAULT 0.00;

-- Or create additional tables for more complex tax handling
CREATE TABLE quote_item_taxes (
    id SERIAL PRIMARY KEY,
    quote_item_id INTEGER REFERENCES quote_items(id),
    tax_rate_id INTEGER REFERENCES tax_rates(id),
    tax_rate NUMERIC(5,2) NOT NULL,
    tax_amount NUMERIC(10,2) NOT NULL
);
```

### Field Name Mismatches
| Diagnostic Expects | Actual Database | Issue |
|-------------------|-----------------|-------|
| `amount` | `total` | Different field name for quote total |
| `balance` | Not present | Field doesn't exist in actual schema |
| `title` | Not present | Field doesn't exist in actual schema |
| `quote_date` | `issue_date` | Different field name |
| `due_date` | `valid_until` | Different field name and purpose |
| `status_id` | `status` | Type mismatch (INTEGER vs VARCHAR) |
| `cost` | `unit_price` | Different field name in quote_items |
| `qty` | `quantity` | Different field name in quote_items |

### Missing Fields in Actual Schema
The diagnostic expects these fields that don't exist in your actual database:
- `quotes.balance`
- `quotes.title` 
- `quotes.tax_rate`
- `quotes.tax_amount`
- `quotes.discount_value`
- `quote_items.tax_rate`
- `quote_items.tax_amount`
- `quote_items.total_amount`

## Immediate Fixes for Your Diagnostic

### 1. Fix Your Test Data Structure
Your diagnostic test data should match the template expectations:

```python
# Test data that matches both your template AND database
quote_test_data = {
    # Core quote fields (database fields)
    'user_id': 1,
    'client_id': 1,  # Ensure this client exists
    'quote_number': 'Q-2025-' + str(int(time.time())),  # Make unique
    'status': 'DRAFT',  # Not status_id!
    'issue_date': '2025-01-15',  # Not quote_date!
    'valid_until': '2025-02-15',  # Not due_date!
    'notes': 'Test quote notes',
    'terms': 'Net 30',
    'subtotal': 200.00,
    'tax_total': 20.00,
    'total': 220.00,
    
    # Items (simplified to match basic database schema)
    'items': [
        {
            # Basic database fields only
            'quote_id': None,  # Set after quote creation
            'product_name': 'Test Product 1',
            'description': 'Test product description',
            'quantity': 2.000,
            'unit_price': 100.00,
            'line_total': 200.00
        }
    ]
}
```

### 2. Update Your Diagnostic Field Validation
Remove validation for these non-existent fields:
- ❌ `amount` (use `total`)
- ❌ `balance` (doesn't exist)  
- ❌ `title` (doesn't exist)
- ❌ `quote_date` (use `issue_date`)
- ❌ `due_date` (use `valid_until`)
- ❌ `status_id` (use `status` as VARCHAR)
- ❌ `cost` (use `unit_price`)
- ❌ `qty` (use `quantity`)

### 3. Database Schema Recommendations
You have two options to fully support your template:

**Option A: Extend Database Schema (Recommended)**
```sql
-- Add missing fields to support template features
ALTER TABLE quote_items ADD COLUMN discount_percentage NUMERIC(5,2) DEFAULT 0.00;
ALTER TABLE quote_items ADD COLUMN tax_rate NUMERIC(5,2) DEFAULT 0.00;
ALTER TABLE quote_items ADD COLUMN tax_amount NUMERIC(10,2) DEFAULT 0.00;
ALTER TABLE quote_items ADD COLUMN discount_amount NUMERIC(10,2) DEFAULT 0.00;

-- Add quote-level discount
ALTER TABLE quotes ADD COLUMN discount_percentage NUMERIC(5,2) DEFAULT 0.00;
ALTER TABLE quotes ADD COLUMN quote_pdf_password VARCHAR(50);
```

**Option B: Use Calculated Fields (Current State)**
Keep your current schema and calculate tax/discount values in your application layer, storing only the final `line_total`.

```python
# Correct data structure based on your Jinja2 template
valid_quote_data = {
    # Required fields from database schema
    'user_id': 1,  # Required field - must exist in users table
    'client_id': 1,  # Must exist in clients table
    'quote_number': 'Q-2025-001',  # Must be unique
    'status': 'DRAFT',  # VARCHAR status (DRAFT, SENT, ACCEPTED, REJECTED, etc.)
    'issue_date': '2025-01-15',  # Date field
    'valid_until': '2025-02-15',  # Expiration date
    
    # Optional fields from template
    'notes': 'Sample quote notes',
    'terms': 'Payment due within 30 days',
    'url_key': None,  # Auto-generated if needed
    'quote_pdf_password': None,  # Optional PDF password
    
    # Financial totals (calculated from items)
    'subtotal': 100.00,
    'tax_total': 10.00,  # Called 'item_tax' in template
    'total': 110.00,
    'discount_percentage': 0.00,  # Quote-level discount percentage
    
    # Items array - matches what template expects
    'items': [
        {
            'quote_id': None,  # Will be set after quote creation
            'product_name': 'Sample Product',  # Called 'name' in template
            'description': 'Product description',
            'quantity': 2.000,  # Decimal field with precision
            'unit_price': 50.00,  # Called 'price' in template  
            'line_total': 100.00,  # Calculated field
            
            # Additional fields from template (may not be in database)
            'discount': 0.00,  # Item-level discount percentage
            'tax_rate': 0.00,  # Tax rate percentage
            'product_id': None,  # Optional reference to products table
            
            # Calculated display fields (from template)
            'subtotal': 100.00,  # quantity * unit_price
            'discount_amount': 0.00,  # subtotal * (discount/100)
            'tax_amount': 0.00,  # (subtotal - discount_amount) * (tax_rate/100)
            'total': 100.00  # subtotal - discount_amount + tax_amount
        }
    ]
}
```

### 3. Update Your Diagnostic Logic
Your diagnostic tool needs to be updated to:

1. **Use correct field names** when validating data
2. **Check against actual database schema** instead of outdated schema file
3. **Validate VARCHAR status values** instead of INTEGER status_id values
4. **Remove validation for non-existent fields** (balance, title, tax fields that don't exist)

### 4. Database Foreign Key Validation
Ensure these reference tables have the required data:
- `users` table must have user with `id = 1`
- `clients` table must have client with `id = 1` 
- Remove checks for `quote_statuses` table since you're using VARCHAR status

## Recommended Action Plan

### Phase 1: Immediate Fixes
1. Update your `quotes_schema.py` file with the correct schema (see below for code example)
2. Fix your test data to use correct field names (see below for code example)
3. Update diagnostic validation logic to match actual database (see below for code example)

```python
# Example: Corrected schema for quotes_schema.py
from sqlalchemy import Column, String, Date, Numeric, Integer, Text
from app.models.base import BaseModel

class Quote(BaseModel):
    __tablename__ = "quotes"
    user_id = Column(Integer, nullable=False)
    client_id = Column(Integer, nullable=False)
    quote_number = Column(String(20), unique=True, nullable=False)
    status = Column(String(20), nullable=False)
    issue_date = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=True)
    notes = Column(Text)
    terms = Column(Text)
    subtotal = Column(Numeric(10,2), default=0)
    tax_total = Column(Numeric(10,2), default=0)
    total = Column(Numeric(10,2), default=0)
    # Add discount_percentage, quote_pdf_password if needed

class QuoteItem(BaseModel):
    __tablename__ = "quote_items"
    quote_id = Column(Integer, nullable=False)
    product_name = Column(String(255), nullable=False)
    description = Column(Text)
    quantity = Column(Numeric(10,3), default=1.000)
    unit_price = Column(Numeric(10,2), nullable=False)
    line_total = Column(Numeric(10,2), nullable=False)
    # Add discount_percentage, tax_rate, tax_amount, discount_amount if needed
```

```python
# Example: Correct test data
quote_test_data = {
    'user_id': 1,
    'client_id': 1,
    'quote_number': 'Q-2025-001',
    'status': 'DRAFT',
    'issue_date': '2025-01-15',
    'valid_until': '2025-02-15',
    'notes': 'Test quote notes',
    'terms': 'Net 30',
    'subtotal': 200.00,
    'tax_total': 20.00,
    'total': 220.00,
    'items': [
        {
            'quote_id': None,
            'product_name': 'Test Product 1',
            'description': 'Test product description',
            'quantity': 2.000,
            'unit_price': 100.00,
            'line_total': 200.00
        }
    ]
}
```

```python
# Example: Diagnostic validation logic
# Remove checks for non-existent fields and use correct names
required_quote_fields = ['user_id', 'client_id', 'quote_number', 'status', 'issue_date', 'valid_until', 'subtotal', 'tax_total', 'total']
required_item_fields = ['quote_id', 'product_name', 'quantity', 'unit_price', 'line_total']
```

### Phase 2: Schema Standardization 
Decide whether to:
- **Option A**: Update database schema to match your diagnostic expectations (see ALTER TABLE examples above)
- **Option B**: Update all code/diagnostics to match current database schema (recommended for stability)

### Phase 3: Data Validation Rules
Update your validation to check:
- `issue_date` ≤ `valid_until` (instead of quote_date/due_date)
- Status values against valid VARCHAR options ('DRAFT', 'SENT', 'ACCEPTED', etc.)
- Remove balance validation (field doesn't exist)
- Focus on subtotal + tax_total = total calculations

```python
# Example: Validation logic
from datetime import datetime

def validate_dates(issue_date, valid_until):
    if valid_until and issue_date > valid_until:
        raise ValueError("issue_date cannot be after valid_until")

def validate_status(status):
    valid_statuses = ['DRAFT', 'SENT', 'ACCEPTED', 'REJECTED', 'EXPIRED', 'CONVERTED']
    if status not in valid_statuses:
        raise ValueError(f"Invalid status: {status}")

def validate_totals(subtotal, tax_total, total):
    if subtotal + tax_total != total:
        raise ValueError("subtotal + tax_total must equal total")
```

## NUMERIC vs DECIMAL Types
The schema mismatch warnings about DECIMAL vs NUMERIC are not critical - these are equivalent in most databases. NUMERIC(10,2) is the correct PostgreSQL syntax.

## Next Steps
1. Run the diagnostic again after updating your schema definition and test data
2. Test with properly structured data that matches your actual database
3. The diagnostic should show significantly fewer issues once the schema alignment is fixed

Your actual database schema looks well-designed and properly normalized. The main issue is that your diagnostic tool is checking against an outdated or incorrect schema specification.
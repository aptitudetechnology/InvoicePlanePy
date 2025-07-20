python3 run_full_quote_diagnostic.py 

============================================================
SETTING UP TEST DATABASE (in-memory SQLite):
============================================================

============================================================
RUNNING DIAGNOSTIC WITH VALID DATA:
============================================================
=== ENHANCED Quote Migration Rollback Diagnostic ===

NOTE: This diagnostic uses the provided IDEAL_QUOTE_SCHEMA (from file) for some checks,
      and also introspects the LIVE DATABASE schema for other checks and the save test.

TOTAL ISSUES FOUND: 18

🚨 CRITICAL - MISSING REQUIRED FIELDS:
   ❌ Missing required field in item[0]: quote_id

⚠️  WARNING - SCHEMA MISMATCHES:
   ⚠️  Schema mismatch: quotes.amount type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quotes.balance type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quotes.tax_rate type mismatch (Ideal: DECIMAL(5,2), Live: NUMERIC(5, 2))
   ⚠️  Schema mismatch: quotes.tax_amount type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quotes.discount_value type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quotes.created_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: quotes.updated_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: quote_items.cost type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quote_items.qty type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quote_items.tax_rate type mismatch (Ideal: DECIMAL(5,2), Live: NUMERIC(5, 2))
   ⚠️  Schema mismatch: quote_items.tax_amount type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quote_items.total_amount type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quote_items.created_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: quote_items.updated_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: quote_custom_fields.created_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: quote_custom_fields.updated_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: products.price type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))

============================================================
TESTING ACTUAL SAVE OPERATION (against live database):
============================================================
✅ Quote save test PASSED

============================================================
FIX RECOMMENDATIONS:
============================================================
🔴 CRITICAL: Add missing required fields to your quote data
   → Missing required field in item[0]: quote_id
⚠️  WARNING: Address schema compatibility issues
   → Your `quotes_schema.py` does not fully match the live database structure.
   → This may indicate outdated documentation or an unexpected database change.
   → Schema mismatch: quotes.amount type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   → Schema mismatch: quotes.balance type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   → Schema mismatch: quotes.tax_rate type mismatch (Ideal: DECIMAL(5,2), Live: NUMERIC(5, 2))

💡 GENERAL RECOMMENDATIONS:
   • Always validate foreign key references (users, clients, products, statuses) before submitting data.
   • Use Decimal types for monetary values to avoid floating-point inaccuracies.
   • Ensure date/datetime objects or correctly formatted strings are used for date fields.
   • Regularly compare your `quotes_schema.py` with your live database schema for consistency.
   • Check your database logs for more detailed error messages if the diagnostic is not specific enough.

============================================================
RUNNING DIAGNOSTIC WITH INTENTIONAL ISSUES:
============================================================
=== ENHANCED Quote Migration Rollback Diagnostic ===

NOTE: This diagnostic uses the provided IDEAL_QUOTE_SCHEMA (from file) for some checks,
      and also introspects the LIVE DATABASE schema for other checks and the save test.

TOTAL ISSUES FOUND: 35

🚨 CRITICAL - MISSING REQUIRED FIELDS:
   ❌ Missing required field in quote: user_id
   ❌ Missing required field in item[0]: quote_id
   ❌ Missing required field in item[0]: product_id
   ❌ Missing required field in item[1]: quote_id

🚨 CRITICAL - FOREIGN KEY VIOLATIONS:
   ❌ Foreign key violation: quote.client_id = '999' not found in clients.id
   ❌ Foreign key violation: quote.status_id = '5' not found in quote_statuses.id

🚨 CRITICAL - DATA TYPE ISSUES:
   ❌ Data type mismatch for item[0].cost: 'abc' (expected DECIMAL(10,2))

⚠️  WARNING - SCHEMA MISMATCHES:
   ⚠️  Schema mismatch: quotes.amount type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quotes.balance type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quotes.tax_rate type mismatch (Ideal: DECIMAL(5,2), Live: NUMERIC(5, 2))
   ⚠️  Schema mismatch: quotes.tax_amount type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quotes.discount_value type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quotes.created_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: quotes.updated_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: quote_items.cost type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quote_items.qty type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quote_items.tax_rate type mismatch (Ideal: DECIMAL(5,2), Live: NUMERIC(5, 2))
   ⚠️  Schema mismatch: quote_items.tax_amount type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quote_items.total_amount type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   ⚠️  Schema mismatch: quote_items.created_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: quote_items.updated_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: quote_custom_fields.created_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: quote_custom_fields.updated_at nullability mismatch (Ideal: NOT NULL, Live: Nullable)
   ⚠️  Schema mismatch: products.price type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))

⚠️  WARNING - CONSTRAINT VIOLATIONS:
   ⚠️  Constraint violation: Duplicate quote_number 'Q-2024-001' already exists (ID: 1)
   ⚠️  Constraint violation: quote.title value too long (300 chars > 255 max)
   ⚠️  Constraint violation: Negative value not allowed for quote.amount: -100.0
   ⚠️  Constraint violation: Negative value not allowed for item[0].qty: -5
   ⚠️  Constraint violation: item[0].qty must be positive: -5
   ⚠️  Constraint violation: item[0].tax_rate out of range (0-100): 120.0
   ⚠️  Constraint violation: item[1].qty must be positive: 0

⚠️  WARNING - BUSINESS LOGIC ISSUES:
   ⚠️  Due date (2024-01-10) cannot be before quote date (2024-01-15)
   ⚠️  Invalid numeric values for cost or qty in item 0 calculation. Cost: abc, Qty: -5
   ⚠️  Balance (5000.00) cannot exceed amount (-100.00)

ℹ️  INFO - TAX RATE ISSUES:
   ℹ️  Item[0] tax rate out of range (0-100): 120.0

============================================================
TESTING ACTUAL SAVE OPERATION (against live database):
============================================================
❌ Quote save test FAILED
   Error Type: IntegrityError
   Rollback Cause: Database constraint violation (foreign key, unique, not null, check constraint)
   Error Message: (sqlite3.IntegrityError) NOT NULL constraint failed: quotes.user_id
[SQL: 
                INSERT INTO quotes (client_id, quote_number, title, quote_date, due_date, amount, balance, status_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ]
[parameters: (999, 'Q-2024-001', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ... (2 characters truncated) ... AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', '2024-01-15', '2024-01-10', -100.0, 5000.0, 5, 'Some notes.')]
(Background on this error at: https://sqlalche.me/e/20/gkpj)
   Detailed Error: {'constraint_type': 'not_null', 'constraint_name': 'Table: quotes, Column: user_id', 'details': "(sqlite3.IntegrityError) NOT NULL constraint failed: quotes.user_id\n[SQL: \n                INSERT INTO quotes (client_id, quote_number, title, quote_date, due_date, amount, balance, status_id, notes)\n                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)\n            ]\n[parameters: (999, 'Q-2024-001', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ... (2 characters truncated) ... AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', '2024-01-15', '2024-01-10', -100.0, 5000.0, 5, 'Some notes.')]\n(Background on this error at: https://sqlalche.me/e/20/gkpj)"}
   SQL Statement: 
                INSERT INTO quotes (client_id, quote_number, title, quote_date, due_date, amount, balance, status_id, notes)
                VALUES (:client_id, :quote_number, :title, :quote_date, :due_date, :amount, :balance, :status_id, :notes)
            
   Parameters: {'client_id': 999, 'quote_number': 'Q-2024-001', 'title': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'quote_date': '2024-01-15', 'due_date': '2024-01-10', 'amount': -100.0, 'balance': 5000.0, 'status_id': 5, 'notes': 'Some notes.'}

============================================================
FIX RECOMMENDATIONS:
============================================================
🔴 CRITICAL: Add missing required fields to your quote data
   → Missing required field in quote: user_id
   → Missing required field in item[0]: quote_id
   → Missing required field in item[0]: product_id
🔴 CRITICAL: Fix foreign key references
   → Verify that referenced IDs exist in related tables (users, clients, products, statuses)
   → Foreign key violation: quote.client_id = '999' not found in clients.id
   → Foreign key violation: quote.status_id = '5' not found in quote_statuses.id
🔴 CRITICAL: Fix data type mismatches
   → Ensure numeric fields contain valid numbers (e.g., '123.45', not 'abc')
   → Verify date/datetime formats (e.g., 'YYYY-MM-DD', 'YYYY-MM-DD HH:MM:SS')
   → Data type mismatch for item[0].cost: 'abc' (expected DECIMAL(10,2))
⚠️  WARNING: Address schema compatibility issues
   → Your `quotes_schema.py` does not fully match the live database structure.
   → This may indicate outdated documentation or an unexpected database change.
   → Schema mismatch: quotes.amount type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   → Schema mismatch: quotes.balance type mismatch (Ideal: DECIMAL(10,2), Live: NUMERIC(10, 2))
   → Schema mismatch: quotes.tax_rate type mismatch (Ideal: DECIMAL(5,2), Live: NUMERIC(5, 2))
⚠️  WARNING: Address other database constraint violations
   → Use unique identifiers (e.g., unique `quote_number`)
   → Shorten string values to fit column length limits (e.g., `VARCHAR(255)`)
   → Ensure amounts, costs, quantities are non-negative
   → Constraint violation: Duplicate quote_number 'Q-2024-001' already exists (ID: 1)
   → Constraint violation: quote.title value too long (300 chars > 255 max)
   → Constraint violation: Negative value not allowed for quote.amount: -100.0
⚠️  WARNING: Fix business logic issues
   → Ensure `due_date` is after `quote_date`
   → Verify `amount` calculations match item totals
   → Ensure `balance` does not exceed `amount`
   → Due date (2024-01-10) cannot be before quote date (2024-01-15)
   → Invalid numeric values for cost or qty in item 0 calculation. Cost: abc, Qty: -5
   → Balance (5000.00) cannot exceed amount (-100.00)
ℹ️  INFO: Review tax rates
   → Ensure tax rates are between 0 and 100.
   → Item[0] tax rate out of range (0-100): 120.0

💡 GENERAL RECOMMENDATIONS:
   • Always validate foreign key references (users, clients, products, statuses) before submitting data.
   • Use Decimal types for monetary values to avoid floating-point inaccuracies.
   • Ensure date/datetime objects or correctly formatted strings are used for date fields.
   • Regularly compare your `quotes_schema.py` with your live database schema for consistency.
   • Check your database logs for more detailed error messages if the diagnostic is not specific enough.

============================================================
DIAGNOSTIC RUN COMPLETE.
============================================================

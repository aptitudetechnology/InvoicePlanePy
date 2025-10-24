QUOTE_SCHEMA = {
    'quotes': {
        'id': {
            'type': 'INTEGER',
            'description': 'Primary key, auto-increment for the quote record.',
            'nullable': False,
            'primary_key': True,
            'auto_increment': True
        },
        'user_id': {
            'type': 'INTEGER',
            'description': 'Foreign key referencing the users table (the user who created the quote).',
            'nullable': False,
            'foreign_key': {'table': 'users', 'column': 'id'}
        },
        'client_id': {
            'type': 'INTEGER',
            'description': 'Foreign key referencing the clients table (the client associated with the quote).',
            'nullable': False,
            'foreign_key': {'table': 'clients', 'column': 'id'}
        },
        'quote_number': {
            'type': 'VARCHAR(50)',
            'description': 'Unique identifier for the quote (e.g., Q-2024-001).',
            'nullable': False,
            'unique': True
        },
        'title': {
            'type': 'VARCHAR(255)',
            'description': 'Title or brief description of the quote.',
            'nullable': True
        },
        'issue_date': {
            'type': 'DATE',
            'description': 'The date the quote was issued.',
            'nullable': False
        },
        'valid_until': {
            'type': 'DATE',
            'description': 'The date by which the quote is expected to be accepted or expire.',
            'nullable': True
        },
        'quote_pdf_password': {
            'type': 'VARCHAR(255)',
            'description': 'Optional password to protect the generated PDF.',
            'nullable': True
        },
        'subtotal': {
            'type': 'DECIMAL(10,2)',
            'description': 'Sum of all item subtotals before quote-level discounts and taxes.',
            'nullable': False,
            'default': 0.00
        },
        'item_tax_total': {
            'type': 'DECIMAL(10,2)',
            'description': 'Total of all item-level taxes.',
            'nullable': False,
            'default': 0.00
        },
        'quote_discount_amount': {
            'type': 'DECIMAL(10,2)',
            'description': 'Quote-level discount amount calculated from discount_percentage.',
            'nullable': False,
            'default': 0.00
        },
        'quote_tax_amount': {
            'type': 'DECIMAL(10,2)',
            'description': 'Quote-level tax amount (applied after discounts).',
            'nullable': False,
            'default': 0.00
        },
        'amount': {
            'type': 'DECIMAL(10,2)',
            'description': 'The final total amount (subtotal - discounts + all taxes).',
            'nullable': False
        },
        'balance': {
            'type': 'DECIMAL(10,2)',
            'description': 'The outstanding balance of the quote (usually same as amount until converted).',
            'nullable': False
        },
        'currency': {
            'type': 'VARCHAR(3)',
            'description': 'The currency code for the quote (e.g., USD, AUD).',
            'nullable': False,
            'default': 'AUD'
        },
        'status_id': {
            'type': 'INTEGER',
            'description': 'Foreign key referencing the quote_statuses table.',
            'nullable': False,
            'foreign_key': {'table': 'quote_statuses', 'column': 'id'},
            'default': 1
        },
        'notes': {
            'type': 'TEXT',
            'description': 'General notes or comments for the entire quote.',
            'nullable': True
        },
        'quote_tax_rate': {
            'type': 'DECIMAL(5,2)',
            'description': 'Quote-level tax rate applied to subtotal after discounts (0-100%).',
            'nullable': False,
            'default': 0.00
        },
        'discount_percentage': {
            'type': 'DECIMAL(5,2)',
            'description': 'Quote-level discount applied to subtotal as percentage (0–100%).',
            'nullable': False,
            'default': 0.00
        },
        'created_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when the quote record was created.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP'
        },
        'updated_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when the quote record was last updated.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
        }
    },
    'quote_items': {
        'id': {
            'type': 'INTEGER',
            'description': 'Primary key, auto-increment for the quote item record.',
            'nullable': False,
            'primary_key': True,
            'auto_increment': True
        },
        'quote_id': {
            'type': 'INTEGER',
            'description': 'Foreign key referencing the quotes table.',
            'nullable': False,
            'foreign_key': {'table': 'quotes', 'column': 'id'}
        },
        'product_id': {
            'type': 'INTEGER',
            'description': 'Foreign key referencing the products table (nullable for custom items).',
            'nullable': True,
            'foreign_key': {'table': 'products', 'column': 'id'}
        },
        'item_name': {
            'type': 'VARCHAR(255)',
            'description': 'Name or description of the item.',
            'nullable': False
        },
        'description': {
            'type': 'TEXT',
            'description': 'Detailed description of the item.',
            'nullable': True
        },
        'unit_price': {
            'type': 'DECIMAL(10,2)',
            'description': 'Unit price of the item.',
            'nullable': False
        },
        'quantity': {
            'type': 'DECIMAL(10,2)',
            'description': 'Quantity of the item.',
            'nullable': False,
            'default': 1.00
        },
        'item_discount_percentage': {
            'type': 'DECIMAL(5,2)',
            'description': 'Discount on this item as a percentage (0–100%).',
            'nullable': False,
            'default': 0.00
        },
        'item_tax_rate': {
            'type': 'DECIMAL(5,2)',
            'description': 'Tax rate specific to this item (0–100%).',
            'nullable': False,
            'default': 0.00
        },
        'subtotal': {
            'type': 'DECIMAL(10,2)',
            'description': 'Calculated: unit_price * quantity',
            'nullable': False
        },
        'discount_amount': {
            'type': 'DECIMAL(10,2)',
            'description': 'Calculated: subtotal * (item_discount_percentage / 100)',
            'nullable': False,
            'default': 0.00
        },
        'taxable_amount': {
            'type': 'DECIMAL(10,2)',
            'description': 'Calculated: subtotal - discount_amount',
            'nullable': False
        },
        'tax_amount': {
            'type': 'DECIMAL(10,2)',
            'description': 'Calculated: taxable_amount * (item_tax_rate / 100)',
            'nullable': False,
            'default': 0.00
        },
        'total': {
            'type': 'DECIMAL(10,2)',
            'description': 'Final item total: taxable_amount + tax_amount',
            'nullable': False
        },
        'sort_order': {
            'type': 'INTEGER',
            'description': 'Display order of the item in the quote.',
            'nullable': False,
            'default': 0
        },
        'created_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when the quote item was created.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP'
        },
        'updated_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when the quote item was last updated.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
        }
    },
    'quote_custom_fields': {
        'id': {
            'type': 'INTEGER',
            'description': 'Primary key, auto-increment.',
            'nullable': False,
            'primary_key': True,
            'auto_increment': True
        },
        'quote_id': {
            'type': 'INTEGER',
            'description': 'Foreign key referencing the quotes table.',
            'nullable': False,
            'foreign_key': {'table': 'quotes', 'column': 'id'}
        },
        'field_name': {
            'type': 'VARCHAR(100)',
            'description': 'Name of the custom field (e.g., "Project_Code").',
            'nullable': False
        },
        'field_value': {
            'type': 'TEXT',
            'description': 'Value of the custom field.',
            'nullable': True
        },
        'field_type': {
            'type': 'VARCHAR(50)',
            'description': 'Data type of the custom field (text, number, date, etc).',
            'nullable': False,
            'default': 'text'
        },
        'created_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when the custom field record was created.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP'
        },
        'updated_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when the custom field record was last updated.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
        }
    },
    'quote_statuses': {
        'id': {
            'type': 'INTEGER',
            'description': 'Primary key, auto-increment.',
            'nullable': False,
            'primary_key': True,
            'auto_increment': True
        },
        'status_name': {
            'type': 'VARCHAR(50)',
            'description': 'Name of the quote status (e.g., "Draft", "Sent", "Accepted", "Declined", "Expired").',
            'nullable': False,
            'unique': True
        },
        'status_code': {
            'type': 'VARCHAR(20)',
            'description': 'Short code for the status (e.g., "draft", "sent", "accepted").',
            'nullable': False,
            'unique': True
        },
        'description': {
            'type': 'TEXT',
            'description': 'Description of the status and its meaning.',
            'nullable': True
        },
        'is_active': {
            'type': 'BOOLEAN',
            'description': 'Whether this status is currently available for use.',
            'nullable': False,
            'default': True
        },
        'sort_order': {
            'type': 'INTEGER',
            'description': 'Display order for status dropdowns.',
            'nullable': False,
            'default': 0
        }
    },
    'tax_rates': {
        'id': {
            'type': 'INTEGER',
            'description': 'Primary key, auto-increment.',
            'nullable': False,
            'primary_key': True,
            'auto_increment': True
        },
        'name': {
            'type': 'VARCHAR(100)',
            'description': 'Name of the tax rate (e.g., "GST", "VAT", "Sales Tax").',
            'nullable': False
        },
        'rate': {
            'type': 'DECIMAL(5,2)',
            'description': 'Tax rate as percentage (0.00 to 100.00).',
            'nullable': False
        },
        'is_active': {
            'type': 'BOOLEAN',
            'description': 'Whether this tax rate is currently available for use.',
            'nullable': False,
            'default': True
        },
        'created_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when the tax rate was created.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP'
        }
    },
    'users': {
        'id': {
            'type': 'INTEGER',
            'description': 'Primary key, auto-increment for users table.',
            'nullable': False,
            'primary_key': True,
            'auto_increment': True
        },
        'name': {
            'type': 'VARCHAR(255)',
            'description': 'User full name.',
            'nullable': False
        },
        'email': {
            'type': 'VARCHAR(255)',
            'description': 'User email address.',
            'nullable': False,
            'unique': True
        },
        'created_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when user was created.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP'
        }
    },
    'clients': {
        'id': {
            'type': 'INTEGER',
            'description': 'Primary key, auto-increment for clients table.',
            'nullable': False,
            'primary_key': True,
            'auto_increment': True
        },
        'name': {
            'type': 'VARCHAR(255)',
            'description': 'Client company or individual name.',
            'nullable': False
        },
        'email': {
            'type': 'VARCHAR(255)',
            'description': 'Primary contact email.',
            'nullable': True
        },
        'phone': {
            'type': 'VARCHAR(50)',
            'description': 'Primary contact phone number.',
            'nullable': True
        },
        'address': {
            'type': 'TEXT',
            'description': 'Street address.',
            'nullable': True
        },
        'city': {
            'type': 'VARCHAR(100)',
            'description': 'City name.',
            'nullable': True
        },
        'state': {
            'type': 'VARCHAR(100)',
            'description': 'State or province.',
            'nullable': True
        },
        'postal_code': {
            'type': 'VARCHAR(20)',
            'description': 'Postal or zip code.',
            'nullable': True
        },
        'country': {
            'type': 'VARCHAR(100)',
            'description': 'Country name.',
            'nullable': True,
            'default': 'Australia'
        },
        'created_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when client was created.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP'
        }
    },
    'products': {
        'id': {
            'type': 'INTEGER',
            'description': 'Primary key, auto-increment for products table.',
            'nullable': False,
            'primary_key': True,
            'auto_increment': True
        },
        'name': {
            'type': 'VARCHAR(255)',
            'description': 'Product or service name.',
            'nullable': False
        },
        'description': {
            'type': 'TEXT',
            'description': 'Detailed product description.',
            'nullable': True
        },
        'sku': {
            'type': 'VARCHAR(100)',
            'description': 'Stock keeping unit or product code.',
            'nullable': True,
            'unique': True
        },
        'unit_price': {
            'type': 'DECIMAL(10,2)',
            'description': 'Default unit price for the product.',
            'nullable': False,
            'default': 0.00
        },
        'default_tax_rate': {
            'type': 'DECIMAL(5,2)',
            'description': 'Default tax rate for this product.',
            'nullable': False,
            'default': 0.00
        },
        'is_active': {
            'type': 'BOOLEAN',
            'description': 'Whether this product is available for selection.',
            'nullable': False,
            'default': True
        },
        'created_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when product was created.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP'
        },
        'updated_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when product was last updated.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
        }
    }
}

# Calculation Logic Documentation:
"""
QUOTE CALCULATION FLOW:

1. ITEM LEVEL:
   - subtotal = unit_price * quantity
   - discount_amount = subtotal * (item_discount_percentage / 100)
   - taxable_amount = subtotal - discount_amount
   - tax_amount = taxable_amount * (item_tax_rate / 100)
   - item_total = taxable_amount + tax_amount

2. QUOTE LEVEL:
   - subtotal = sum(all item.subtotal)
   - item_tax_total = sum(all item.tax_amount)
   - quote_discount_amount = subtotal * (discount_percentage / 100)
   - quote_tax_amount = (subtotal - quote_discount_amount) * (quote_tax_rate / 100)
   - amount = subtotal - quote_discount_amount + item_tax_total + quote_tax_amount
   - balance = amount (initially, until payments applied)

EXAMPLE STATUS RECORDS:
INSERT INTO quote_statuses (status_name, status_code, description, sort_order) VALUES
('Draft', 'draft', 'Quote is being prepared and not yet sent', 1),
('Sent', 'sent', 'Quote has been sent to client', 2),
('Accepted', 'accepted', 'Client has accepted the quote', 3),
('Declined', 'declined', 'Client has declined the quote', 4),
('Expired', 'expired', 'Quote has passed its valid_until date', 5);

EXAMPLE TAX RATES:
INSERT INTO tax_rates (name, rate) VALUES
('GST', 10.00),
('No Tax', 0.00),
('Reduced Rate', 5.00);
"""
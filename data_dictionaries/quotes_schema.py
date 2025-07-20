"""
This module defines a conceptual schema for the 'quotes' and related tables.
It's intended for documentation, static validation, or to guide the creation
of actual database tables.

NOTE: The ImprovedQuoteRollbackDiagnostic script primarily uses introspection
to get the *actual* database schema at runtime. This file serves as a
reference or a target schema definition.
"""

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
        'quote_date': {
            'type': 'DATE',
            'description': 'The date the quote was issued.',
            'nullable': False
        },
        'due_date': {
            'type': 'DATE',
            'description': 'The date by which the quote is expected to be accepted or payment is due.',
            'nullable': True
        },
        'amount': {
            'type': 'DECIMAL(10,2)',
            'description': 'The total calculated amount of the quote, including items and tax.',
            'nullable': False
        },
        'balance': {
            'type': 'DECIMAL(10,2)',
            'description': 'The outstanding balance of the quote.',
            'nullable': False
        },
        'currency': {
            'type': 'VARCHAR(3)',
            'description': 'The currency code for the quote (e.g., USD, AUD).',
            'nullable': True,
            'default': 'AUD'
        },
        'status_id': {
            'type': 'INTEGER',
            'description': 'Foreign key referencing the quote_statuses table (e.g., Draft, Sent, Accepted, Rejected).',
            'nullable': False,
            'foreign_key': {'table': 'quote_statuses', 'column': 'id'}
        },
        'notes': {
            'type': 'TEXT',
            'description': 'General notes or comments for the entire quote.',
            'nullable': True
        },
        'tax_rate': { # Main quote tax rate, if applicable (can be overridden by item tax rates)
            'type': 'DECIMAL(5,2)',
            'description': 'Default tax rate for the entire quote (0-100%).',
            'nullable': True,
            'default': 0.00
        },
        'tax_amount': {
            'type': 'DECIMAL(10,2)',
            'description': 'Calculated total tax amount for the quote.',
            'nullable': True
        },
        'discount_type': {
            'type': 'VARCHAR(20)', # e.g., 'percentage', 'fixed'
            'description': 'Type of discount applied (e.g., percentage, fixed amount).',
            'nullable': True
        },
        'discount_value': {
            'type': 'DECIMAL(10,2)',
            'description': 'Value of the discount applied (percentage or fixed amount).',
            'nullable': True
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
            'description': 'Foreign key referencing the products table (the product or service being quoted).',
            'nullable': False,
            'foreign_key': {'table': 'products', 'column': 'id'}
        },
        'item_name': {
            'type': 'VARCHAR(255)',
            'description': 'Name or description of the item.',
            'nullable': True # Can be derived from product_id or custom
        },
        'description': {
            'type': 'TEXT',
            'description': 'Detailed description of the quote item.',
            'nullable': True
        },
        'cost': {
            'type': 'DECIMAL(10,2)',
            'description': 'Unit cost of the product or service.',
            'nullable': False
        },
        'qty': {
            'type': 'DECIMAL(10,2)',
            'description': 'Quantity of the product or service.',
            'nullable': False
        },
        'tax_rate': {
            'type': 'DECIMAL(5,2)',
            'description': 'Tax rate specific to this item (0-100%). Overrides quote default if present.',
            'nullable': True,
            'default': 0.00
        },
        'tax_amount': {
            'type': 'DECIMAL(10,2)',
            'description': 'Calculated tax amount for this specific item.',
            'nullable': True
        },
        'total_amount': {
            'type': 'DECIMAL(10,2)',
            'description': 'Total amount for this item (cost * qty + tax_amount).',
            'nullable': True
        },
        'notes': {
            'type': 'TEXT',
            'description': 'Specific notes for this individual quote item.',
            'nullable': True
        },
        'sort_order': {
            'type': 'INTEGER',
            'description': 'Order of the item within the quote for display purposes.',
            'nullable': True
        },
        'created_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when the quote item record was created.',
            'nullable': False,
            'default': 'CURRENT_TIMESTAMP'
        },
        'updated_at': {
            'type': 'DATETIME',
            'description': 'Timestamp when the quote item record was last updated.',
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
            'type': 'VARCHAR(50)', # e.g., 'text', 'number', 'date'
            'description': 'Data type of the custom field value.',
            'nullable': True
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
            'description': 'Name of the quote status (e.g., "Draft", "Sent", "Accepted", "Rejected", "Expired").',
            'nullable': False,
            'unique': True
        },
        'description': {
            'type': 'TEXT',
            'description': 'Description of the status.',
            'nullable': True
        }
    },
    # Add other related tables here if you want a truly comprehensive schema
    # For example, 'users', 'clients', 'products'
    'users': {
        'id': {
            'type': 'INTEGER',
            'description': 'Primary key, auto-increment for users table.',
            'nullable': False, 'primary_key': True, 'auto_increment': True
        },
        'name': {'type': 'VARCHAR(255)', 'description': 'User full name.', 'nullable': False},
        'email': {'type': 'VARCHAR(255)', 'description': 'User email.', 'nullable': False, 'unique': True},
        # ... other user fields
    },
    'clients': {
        'id': {
            'type': 'INTEGER',
            'description': 'Primary key, auto-increment for clients table.',
            'nullable': False, 'primary_key': True, 'auto_increment': True
        },
        'name': {'type': 'VARCHAR(255)', 'description': 'Client full name or company name.', 'nullable': False},
        'email': {'type': 'VARCHAR(255)', 'description': 'Client contact email.', 'nullable': True},
        # ... other client fields
    },
    'products': {
        'id': {
            'type': 'INTEGER',
            'description': 'Primary key, auto-increment for products table.',
            'nullable': False, 'primary_key': True, 'auto_increment': True
        },
        'name': {'type': 'VARCHAR(255)', 'description': 'Product or service name.', 'nullable': False},
        'price': {'type': 'DECIMAL(10,2)', 'description': 'Default price of the product.', 'nullable': True},
        # ... other product fields
    }
}
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
        'issue_date': {  # renamed from quote_date
            'type': 'DATE',
            'description': 'The date the quote was issued.',
            'nullable': False
        },
        'valid_until': {  # renamed from due_date
            'type': 'DATE',
            'description': 'The date by which the quote is expected to be accepted or expire.',
            'nullable': True
        },
        'quote_pdf_password': {  # newly added
            'type': 'VARCHAR(255)',
            'description': 'Optional password to protect the generated PDF.',
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
            'description': 'Foreign key referencing the quote_statuses table.',
            'nullable': False,
            'foreign_key': {'table': 'quote_statuses', 'column': 'id'}
        },
        'notes': {
            'type': 'TEXT',
            'description': 'General notes or comments for the entire quote.',
            'nullable': True
        },
        'tax_rate': {
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
        'discount_percentage': {  # replaces discount_type and discount_value
            'type': 'DECIMAL(5,2)',
            'description': 'Discount applied to the subtotal as a percentage (0–100%).',
            'nullable': True,
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
            'description': 'Foreign key referencing the products table.',
            'nullable': True,
            'foreign_key': {'table': 'products', 'column': 'id'}
        },
        'item_name': {
            'type': 'VARCHAR(255)',
            'description': 'Name or description of the item.',
            'nullable': True
        },
        'description': {
            'type': 'TEXT',
            'description': 'Detailed description of the item.',
            'nullable': True
        },
        'price': {  # renamed from cost
            'type': 'DECIMAL(10,2)',
            'description': 'Unit price of the item.',
            'nullable': False
        },
        'quantity': {  # renamed from qty
            'type': 'DECIMAL(10,2)',
            'description': 'Quantity of the item.',
            'nullable': False
        },
        'discount': {  # newly added
            'type': 'DECIMAL(5,2)',
            'description': 'Discount on this item as a percentage (0–100%).',
            'nullable': True,
            'default': 0.00
        },
        'tax_rate': {
            'type': 'DECIMAL(5,2)',
            'description': 'Tax rate specific to this item.',
            'nullable': True,
            'default': 0.00
        },
        'tax_amount': {
            'type': 'DECIMAL(10,2)',
            'description': 'Tax amount for the item.',
            'nullable': True
        },
        'subtotal': {  # newly added
            'type': 'DECIMAL(10,2)',
            'description': 'Subtotal before discount and tax (price * quantity).',
            'nullable': True
        },
        'discount_amount': {  # newly added
            'type': 'DECIMAL(10,2)',
            'description': 'Discount amount applied to the item.',
            'nullable': True
        },
        'total': {  # renamed from total_amount
            'type': 'DECIMAL(10,2)',
            'description': 'Final total after tax and discount.',
            'nullable': True
        },
        'sort_order': {
            'type': 'INTEGER',
            'description': 'Display order of the item in the quote.',
            'nullable': True
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
            'description': 'Data type of the custom field.',
            'nullable': True
        },
        'created_at':_

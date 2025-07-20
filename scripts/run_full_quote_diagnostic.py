import logging
import traceback
from decimal import Decimal, InvalidOperation
from datetime import datetime
from sqlalchemy import inspect, text, event, create_engine, Column, Integer, String, Date, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.exc import IntegrityError, DatabaseError, StatementError
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Dict, List, Any, Optional
import json
import re
import sys
import os

# --- Import the ideal schema from your data_dictionaries folder ---
# This assumes your project structure is:
# /app
#   ├── data_dictionaries/
#   │   └── quotes_schema.py
#   └── scripts/
#       └── quote_diagnostic.py (this file)
# Add /app to sys.path so we can import from data_dictionaries
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    from data_dictionaries.quotes_schema import QUOTE_SCHEMA as IDEAL_QUOTE_SCHEMA
except ImportError:
    print("ERROR: Could not import QUOTE_SCHEMA from data_dictionaries/quotes_schema.py")
    print("Please ensure the 'data_dictionaries' folder and 'quotes_schema.py' file exist directly under /app.")
    print("Or adjust the sys.path.append if your structure is different.")
    IDEAL_QUOTE_SCHEMA = {} # Fallback to empty schema if import fails

class ImprovedQuoteRollbackDiagnostic:
    def __init__(self, engine, session_factory, ideal_schema: Dict[str, Any]):
        self.engine = engine
        self.Session = session_factory
        self.logger = logging.getLogger(__name__)
        self.ideal_schema = ideal_schema # The schema loaded from quotes_schema.py
        self.live_db_schema = self._get_live_db_schema() # The schema introspected from the live DB

    def _get_live_db_schema(self) -> Dict[str, Any]:
        """Get actual database schema by introspecting the live database"""
        inspector = inspect(self.engine)
        schema = {}
        try:
            for table_name in inspector.get_table_names():
                columns = inspector.get_columns(table_name)
                # For SQLite, get_pk_constraint might return an empty dict if no PK is explicitly defined
                pk_constraint = inspector.get_pk_constraint(table_name)
                schema[table_name] = {
                    'columns': [col['name'] for col in columns],
                    'column_details': {col['name']: col for col in columns},
                    'primary_keys': pk_constraint['constrained_columns'] if pk_constraint else [],
                    'foreign_keys': [fk for fk in inspector.get_foreign_keys(table_name)]
                }
        except Exception as e:
            self.logger.error(f"Error retrieving live database schema: {str(e)}")
        return schema

    def diagnose_rollback_causes(self, quote_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Enhanced diagnostic for quote rollback causes"""
        issues = {
            'missing_required_fields': [],
            'foreign_key_violations': [],
            'custom_field_issues': [],
            'tax_rate_issues': [],
            'constraint_violations': [],
            'schema_mismatches': [], # New category for ideal vs live DB schema comparison
            'data_type_issues': [],
            'circular_dependencies': [],
            'transaction_issues': [], # Captured during actual save test
            'business_logic_issues': []
        }

        # Enhanced checks, now leveraging ideal_schema where appropriate
        issues['missing_required_fields'] = self._check_required_fields_enhanced(quote_data)
        issues['data_type_issues'] = self._check_data_types(quote_data)
        issues['constraint_violations'].extend(self._check_constraints_enhanced(quote_data)) # Add from updated check
        
        # These still need live DB interaction or specific checks
        issues['foreign_key_violations'] = self._check_foreign_keys_enhanced(quote_data)
        issues['custom_field_issues'] = self._check_custom_fields(quote_data)
        issues['tax_rate_issues'] = self._check_tax_rates(quote_data)
        issues['circular_dependencies'] = self._check_circular_dependencies(quote_data)
        issues['business_logic_issues'] = self._check_business_logic(quote_data)
        issues['schema_mismatches'] = self._check_schema_compatibility_enhanced() # New check

        return issues

    def _get_column_info_from_schema(self, table_name: str, col_name: str) -> Optional[Dict[str, Any]]:
        """Helper to get column info from either ideal or live DB schema."""
        # Prioritize ideal schema if available and column exists there
        if table_name in self.ideal_schema and col_name in self.ideal_schema[table_name]:
            return self.ideal_schema[table_name][col_name]
        # Fallback to live DB schema
        if table_name in self.live_db_schema and col_name in self.live_db_schema[table_name]['column_details']:
            return self.live_db_schema[table_name]['column_details'][col_name]
        return None

    def _check_required_fields_enhanced(self, quote_data: Dict[str, Any]) -> List[str]:
        """Enhanced required fields check using ideal schema first, then live DB schema"""
        issues = []

        # Helper to check a table's required fields
        def _check_table_required_fields(data: Dict[str, Any], table_name: str, context: str):
            schema_to_use = self.ideal_schema.get(table_name) or self.live_db_schema.get(table_name, {}).get('column_details')
            if not schema_to_use:
                return # No schema info for this table

            for col_name, col_info in schema_to_use.items():
                is_nullable = col_info.get('nullable', True) # Default to nullable if not specified
                has_default = col_info.get('default') is not None # Check for 'default' key presence
                is_auto_generated = col_name in ['id', 'created_at', 'updated_at'] # Common auto-generated

                if not is_nullable and not has_default and not is_auto_generated:
                    if col_name not in data or data.get(col_name) is None or (isinstance(data.get(col_name), str) and not data.get(col_name).strip()):
                        issues.append(f"Missing required field in {context}: {col_name}")

        _check_table_required_fields(quote_data, 'quotes', 'quote')

        items = quote_data.get('items', [])
        for i, item in enumerate(items):
            _check_table_required_fields(item, 'quote_items', f'item[{i}]')

        return issues

    def _check_foreign_keys_enhanced(self, quote_data: Dict[str, Any]) -> List[str]:
        """Enhanced foreign key check with batch validation against live DB"""
        issues = []
        session = self.Session()

        try:
            fk_checks = []

            # Check quote foreign keys
            # Prioritize ideal schema FKs, fallback to live DB FKs if not defined in ideal
            quote_fks = self.ideal_schema.get('quotes', {}).get('foreign_keys')
            if quote_fks is None: # If not explicitly defined in ideal, use live DB
                quote_fks = self.live_db_schema.get('quotes', {}).get('foreign_keys', [])

            for col_info in self.ideal_schema.get('quotes', {}).values():
                if 'foreign_key' in col_info:
                    col_name = col_info['name'] if 'name' in col_info else [k for k,v in self.ideal_schema['quotes'].items() if v==col_info][0] # Attempt to get col name
                    ref_table = col_info['foreign_key']['table']
                    ref_col = col_info['foreign_key']['column']
                    if quote_data.get(col_name) is not None:
                        fk_checks.append({
                            'value': quote_data[col_name],
                            'table': ref_table,
                            'column': ref_col,
                            'source': f'quote.{col_name}'
                        })

            # Add foreign keys discovered from live DB if not already covered by ideal schema
            if 'quotes' in self.live_db_schema:
                for fk in self.live_db_schema['quotes']['foreign_keys']:
                    col_name = fk['constrained_columns'][0]
                    ref_table = fk['referred_table']
                    ref_col = fk['referred_columns'][0]
                    # Ensure we don't duplicate checks if already handled by ideal_schema
                    if not any(c['source'] == f'quote.{col_name}' for c in fk_checks):
                        if quote_data.get(col_name) is not None:
                            fk_checks.append({
                                'value': quote_data[col_name],
                                'table': ref_table,
                                'column': ref_col,
                                'source': f'quote.{col_name}'
                            })


            # Check item foreign keys
            items = quote_data.get('items', [])
            item_fks = self.ideal_schema.get('quote_items', {}).get('foreign_keys')
            if item_fks is None:
                item_fks = self.live_db_schema.get('quote_items', {}).get('foreign_keys', [])

            for i, item in enumerate(items):
                for col_info in self.ideal_schema.get('quote_items', {}).values():
                    if 'foreign_key' in col_info:
                        col_name = col_info['name'] if 'name' in col_info else [k for k,v in self.ideal_schema['quote_items'].items() if v==col_info][0]
                        ref_table = col_info['foreign_key']['table']
                        ref_col = col_info['foreign_key']['column']
                        if item.get(col_name) is not None:
                            fk_checks.append({
                                'value': item[col_name],
                                'table': ref_table,
                                'column': ref_col,
                                'source': f'item[{i}].{col_name}'
                            })
                
                # Add foreign keys discovered from live DB if not already covered by ideal schema
                if 'quote_items' in self.live_db_schema:
                    for fk in self.live_db_schema['quote_items']['foreign_keys']:
                        col_name = fk['constrained_columns'][0]
                        ref_table = fk['referred_table']
                        ref_col = fk['referred_columns'][0]
                        if not any(c['source'] == f'item[{i}].{col_name}' for c in fk_checks if f'item[{i}]' in c['source']):
                            if item.get(col_name) is not None:
                                fk_checks.append({
                                    'value': item[col_name],
                                    'table': ref_table,
                                    'column': ref_col,
                                    'source': f'item[{i}].{col_name}'
                                })


            # Batch validate foreign keys against the live database
            for check in fk_checks:
                if check['value'] is None: # Skip if FK value is null, unless it's a NOT NULL constraint
                    continue
                try:
                    result = session.execute(
                        text(f"SELECT 1 FROM {check['table']} WHERE {check['column']} = :value LIMIT 1"),
                        {'value': check['value']}
                    ).fetchone()

                    if not result:
                        issues.append(f"Foreign key violation: {check['source']} = '{check['value']}' not found in {check['table']}.{check['column']}")
                except Exception as e:
                    issues.append(f"Error checking foreign key {check['source']}: {str(e)}")

        except Exception as e:
            issues.append(f"Error in foreign key validation setup: {str(e)}")
        finally:
            session.close()

        return issues

    def _check_custom_fields(self, quote_data: Dict[str, Any]) -> List[str]:
        """Check custom field issues using ideal schema if available, else basic checks."""
        issues = []
        custom_fields = quote_data.get('custom_fields', {})

        if custom_fields:
            # Check if custom fields table is expected in ideal schema or found in live DB
            custom_table_exists_expected = 'quote_custom_fields' in self.ideal_schema
            custom_table_exists_live = 'quote_custom_fields' in self.live_db_schema

            if not custom_table_exists_expected and not custom_table_exists_live:
                issues.append("Custom fields data provided but 'quote_custom_fields' table not defined in ideal schema and not found in live database.")
                return issues # No further checks if table doesn't exist

            # Get schema info for custom fields
            custom_field_schema = self.ideal_schema.get('quote_custom_fields') or \
                                  self.live_db_schema.get('quote_custom_fields', {}).get('column_details')

            if not custom_field_schema: # Fallback if no schema info available
                issues.append("Warning: No schema definition found for 'quote_custom_fields' to perform detailed validation.")
                for field_name, field_value in custom_fields.items():
                    if not isinstance(field_name, str) or len(field_name.strip()) == 0:
                        issues.append(f"Invalid custom field name: {field_name} (must be a non-empty string)")
                    if isinstance(field_value, str) and len(field_value) > 1000: # Arbitrary fallback limit
                        issues.append(f"Custom field value too long for {field_name}: {len(field_value)} chars (exceeds fallback 1000 chars)")
            else:
                field_name_col = custom_field_schema.get('field_name')
                field_value_col = custom_field_schema.get('field_value')

                max_field_name_len = None
                if field_name_col and 'VARCHAR' in field_name_col.get('type', '').upper():
                    match = re.search(r'\((\d+)\)', field_name_col['type'])
                    if match: max_field_name_len = int(match.group(1))

                max_field_value_len = None
                if field_value_col and 'VARCHAR' in field_value_col.get('type', '').upper():
                    match = re.search(r'\((\d+)\)', field_value_col['type'])
                    if match: max_field_value_len = int(match.group(1))

                for field_name, field_value in custom_fields.items():
                    if not isinstance(field_name, str) or len(field_name.strip()) == 0:
                        issues.append(f"Invalid custom field name: {field_name} (must be a non-empty string)")
                    elif max_field_name_len and len(field_name) > max_field_name_len:
                        issues.append(f"Custom field name too long: '{field_name}' ({len(field_name)} chars > {max_field_name_len} max)")

                    if isinstance(field_value, str) and max_field_value_len and len(field_value) > max_field_value_len:
                        issues.append(f"Custom field value too long for {field_name}: {len(field_value)} chars > {max_field_value_len} max")
                    # Could add type checking for custom fields too if a 'field_type' column is consistently used and mapped to a type.

        return issues

    def _check_tax_rates(self, quote_data: Dict[str, Any]) -> List[str]:
        """Check tax rate related issues"""
        issues = []

        def validate_tax_rate(rate_value, context_name):
            if rate_value is None: return
            try:
                tax_rate = float(rate_value)
                if tax_rate < 0 or tax_rate > 100:
                    issues.append(f"{context_name} tax rate out of range (0-100): {rate_value}")
            except (ValueError, TypeError):
                issues.append(f"Invalid tax rate format for {context_name}: {rate_value}")

        validate_tax_rate(quote_data.get('tax_rate'), 'Quote')

        items = quote_data.get('items', [])
        for i, item in enumerate(items):
            validate_tax_rate(item.get('tax_rate'), f"Item[{i}]")

        return issues

    def _check_business_logic(self, quote_data: Dict[str, Any]) -> List[str]:
        """Check business logic constraints"""
        issues = []

        # Check date logic
        quote_date = quote_data.get('quote_date')
        due_date = quote_data.get('due_date')

        if quote_date and due_date:
            try:
                # Ensure conversion to datetime objects for comparison
                q_date = datetime.strptime(str(quote_date), '%Y-%m-%d').date() if isinstance(quote_date, (str, datetime)) else quote_date.date()
                d_date = datetime.strptime(str(due_date), '%Y-%m-%d').date() if isinstance(due_date, (str, datetime)) else due_date.date()

                if d_date < q_date:
                    issues.append(f"Due date ({due_date}) cannot be before quote date ({quote_date})")
            except ValueError:
                issues.append(f"Invalid date format in quote_date ({quote_date}) or due_date ({due_date})")
            except AttributeError:
                issues.append(f"Date values (quote_date: {quote_date}, due_date: {due_date}) are not in expected format for comparison.")


        # Check amount calculations (only if amount is provided and is a number)
        items = quote_data.get('items', [])
        calculated_total = Decimal('0.00')
        item_calculation_error = False

        if items:
            for i, item in enumerate(items):
                try:
                    cost = Decimal(str(item.get('cost', 0)))
                    qty = Decimal(str(item.get('qty', 0))) # Use 0 for qty if missing/invalid to avoid breaking sum
                    calculated_total += cost * qty
                except (ValueError, InvalidOperation, TypeError):
                    issues.append(f"Invalid numeric values for cost or qty in item {i} calculation. Cost: {item.get('cost')}, Qty: {item.get('qty')}")
                    item_calculation_error = True
            
            quote_amount = quote_data.get('amount')
            if quote_amount is not None and not item_calculation_error: # Only check if quote_amount exists and no item calc errors
                try:
                    amount_decimal = Decimal(str(quote_amount))
                    amount_diff = abs(amount_decimal - calculated_total)
                    # Allow for small rounding differences (e.g., 2 decimal places precision)
                    if amount_diff > Decimal('0.01'):
                        issues.append(f"Quote amount ({amount_decimal:.2f}) doesn't match calculated total ({calculated_total:.2f}) from items. Difference: {amount_diff:.2f}")
                except (ValueError, InvalidOperation, TypeError):
                    issues.append(f"Invalid numeric value for quote amount: {quote_amount}")


        # Check balance logic
        amount = quote_data.get('amount')
        balance = quote_data.get('balance')
        if amount is not None and balance is not None:
            try:
                amount_decimal = Decimal(str(amount))
                balance_decimal = Decimal(str(balance))
                if balance_decimal > amount_decimal:
                    issues.append(f"Balance ({balance_decimal:.2f}) cannot exceed amount ({amount_decimal:.2f})")
            except (ValueError, InvalidOperation, TypeError):
                issues.append(f"Invalid numeric values for amount ({amount}) or balance ({balance}) in balance logic check.")

        return issues

    def _check_data_types(self, quote_data: Dict[str, Any]) -> List[str]:
        """Check for data type mismatches against ideal schema, falling back to live DB schema"""
        issues = []

        def validate_field_type(value, table_name, field_name, context_prefix):
            col_info = self._get_column_info_from_schema(table_name, field_name)
            if not col_info:
                # If column not found in any schema, skip type validation (might be an extra field)
                return

            expected_type_str = str(col_info.get('type', 'UNKNOWN')).upper()
            if value is None and not col_info.get('nullable', True):
                # This is a missing required field, handled by _check_required_fields_enhanced
                return

            if value is None: # Null values are fine if nullable
                return

            try:
                if any(t in expected_type_str for t in ['INT', 'INTEGER']):
                    if not isinstance(value, (int, float)) or not float(value).is_integer():
                        issues.append(f"Data type mismatch for {context_prefix}{field_name}: '{value}' (expected INTEGER)")
                elif any(t in expected_type_str for t in ['DECIMAL', 'NUMERIC', 'FLOAT', 'DOUBLE', 'REAL']):
                    Decimal(str(value)) # Try converting to Decimal, handles floats and strings
                elif 'DATE' in expected_type_str and 'TIME' not in expected_type_str:
                    if isinstance(value, str):
                        datetime.strptime(value, '%Y-%m-%d').date()
                    elif not isinstance(value, (datetime, datetime.date)):
                         issues.append(f"Data type mismatch for {context_prefix}{field_name}: '{value}' (expected DATE)")
                elif any(t in expected_type_str for t in ['TIMESTAMP', 'DATETIME']):
                    if isinstance(value, str):
                        # Attempt common datetime formats
                        try:
                            datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            datetime.strptime(value, '%Y-%m-%dT%H:%M:%S') # ISO format
                    elif not isinstance(value, datetime):
                        issues.append(f"Data type mismatch for {context_prefix}{field_name}: '{value}' (expected DATETIME/TIMESTAMP)")
                elif any(t in expected_type_str for t in ['VARCHAR', 'CHAR', 'TEXT']):
                    if not isinstance(value, (str, type(None))):
                        issues.append(f"Data type mismatch for {context_prefix}{field_name}: '{value}' (expected STRING/TEXT)")
                elif 'BOOLEAN' in expected_type_str:
                    if not isinstance(value, bool) and value not in [0, 1]:
                        issues.append(f"Data type mismatch for {context_prefix}{field_name}: '{value}' (expected BOOLEAN/0/1)")

            except (ValueError, InvalidOperation, TypeError):
                issues.append(f"Data type mismatch for {context_prefix}{field_name}: '{value}' (expected {expected_type_str})")

        # Check quote data types
        for field_name, value in quote_data.items():
            validate_field_type(value, 'quotes', field_name, 'quote.')

        # Check item data types
        items = quote_data.get('items', [])
        for i, item in enumerate(items):
            for field_name, value in item.items():
                validate_field_type(value, 'quote_items', field_name, f'item[{i}].')

        # Check custom field values (assuming field_value column in custom_fields table)
        custom_fields_data = quote_data.get('custom_fields', {})
        if custom_fields_data and ('quote_custom_fields' in self.ideal_schema or 'quote_custom_fields' in self.live_db_schema):
            field_value_col_info = self._get_column_info_from_schema('quote_custom_fields', 'field_value')
            if field_value_col_info:
                field_value_expected_type = str(field_value_col_info.get('type', 'TEXT')).upper()
                for field_name, field_value in custom_fields_data.items():
                    # If the ideal_schema specifies a field_type for custom fields, could add more specific validation here.
                    # For now, just check against the generic 'field_value' column type.
                    validate_field_type(field_value, 'quote_custom_fields', 'field_value', f"custom_fields['{field_name}'].")


        return issues

    def _check_constraints_enhanced(self, quote_data: Dict[str, Any]) -> List[str]:
        """Enhanced constraint checking using ideal schema for lengths and numeric ranges,
           and live DB for unique constraints."""
        issues = []
        session = self.Session()

        try:
            # Check unique constraints against live DB
            # This is specific to 'quote_number' for 'quotes' table, expand if other unique constraints exist
            if 'quotes' in self.live_db_schema and quote_data.get('quote_number'):
                # More sophisticated duplicate check: exclude itself if updating an existing quote
                query = text("""
                    SELECT id, quote_number FROM quotes
                    WHERE quote_number = :quote_number
                    AND (:quote_id IS NULL OR id != :quote_id)
                """)
                result = session.execute(query, {
                    'quote_number': quote_data['quote_number'],
                    'quote_id': quote_data.get('id') # Pass existing ID if present
                }).fetchone()

                if result:
                    issues.append(f"Constraint violation: Duplicate quote_number '{quote_data['quote_number']}' already exists (ID: {result[0]})")

            # Check string length constraints (using ideal schema preferentially)
            def check_string_lengths(data_dict: Dict[str, Any], table_name: str, context: str):
                schema_to_use = self.ideal_schema.get(table_name) or self.live_db_schema.get(table_name, {}).get('column_details')
                if not schema_to_use: return

                for field_name, value in data_dict.items():
                    if isinstance(value, str):
                        col_info = schema_to_use.get(field_name) # From ideal
                        if not col_info and table_name in self.live_db_schema: # Fallback to live DB column_details
                            col_info = self.live_db_schema[table_name]['column_details'].get(field_name)

                        if col_info:
                            col_type = str(col_info.get('type', '')).upper()
                            if 'VARCHAR' in col_type or 'CHAR' in col_type:
                                match = re.search(r'\((\d+)\)', col_type)
                                if match:
                                    max_length = int(match.group(1))
                                    if len(value) > max_length:
                                        issues.append(f"Constraint violation: {context}.{field_name} value too long ({len(value)} chars > {max_length} max)")

            check_string_lengths(quote_data, 'quotes', 'quote')
            items = quote_data.get('items', [])
            for i, item in enumerate(items):
                check_string_lengths(item, 'quote_items', f'item[{i}]')
            if quote_data.get('custom_fields'):
                custom_fields_data = quote_data['custom_fields']
                for field_name, field_value in custom_fields_data.items():
                    # For custom fields, check the field_name and field_value columns
                    check_string_lengths({field_name: field_name}, 'quote_custom_fields', f"custom_field_name['{field_name}']")
                    if isinstance(field_value, str):
                         # Get 'field_value' column info for its length
                        field_value_col_info = self._get_column_info_from_schema('quote_custom_fields', 'field_value')
                        if field_value_col_info:
                            col_type = str(field_value_col_info.get('type', '')).upper()
                            if 'VARCHAR' in col_type or 'CHAR' in col_type:
                                match = re.search(r'\((\d+)\)', col_type)
                                if match:
                                    max_length = int(match.group(1))
                                    if len(field_value) > max_length:
                                        issues.append(f"Constraint violation: custom_field_value for '{field_name}' too long ({len(field_value)} chars > {max_length} max)")


            # Check numeric ranges (using ideal schema for type info if available)
            numeric_fields = {
                'quotes': ['amount', 'balance', 'tax_rate', 'discount_value'],
                'quote_items': ['cost', 'qty', 'tax_rate'],
            }

            def check_numeric_ranges(data_dict: Dict[str, Any], table_name: str, context: str):
                schema_cols = self.ideal_schema.get(table_name) or \
                              (self.live_db_schema.get(table_name, {}).get('column_details'))
                if not schema_cols: return

                for field_name in numeric_fields.get(table_name, []):
                    if field_name in data_dict and data_dict[field_name] is not None:
                        try:
                            val = Decimal(str(data_dict[field_name]))
                            # Check for negative values for specific fields
                            if field_name in ['amount', 'balance', 'cost', 'qty', 'discount_value'] and val < 0:
                                issues.append(f"Constraint violation: Negative value not allowed for {context}.{field_name}: {val}")
                            # Check tax rate range
                            if field_name == 'tax_rate' and (val < 0 or val > 100):
                                issues.append(f"Constraint violation: {context}.{field_name} out of range (0-100): {val}")
                            # Add more specific range checks if needed (e.g., qty > 0)
                            if field_name == 'qty' and val <= 0:
                                issues.append(f"Constraint violation: {context}.{field_name} must be positive: {val}")
                        except (ValueError, InvalidOperation, TypeError):
                            # This case is primarily handled by _check_data_types
                            pass

            check_numeric_ranges(quote_data, 'quotes', 'quote')
            for i, item in enumerate(items):
                check_numeric_ranges(item, 'quote_items', f'item[{i}]')

        except Exception as e:
            issues.append(f"Error checking constraints: {str(e)}")
        finally:
            session.close()

        return issues

    def _check_circular_dependencies(self, quote_data: Dict[str, Any]) -> List[str]:
        """Check for simple circular dependency issues (e.g., quote ID used as product ID in its own items)"""
        issues = []
        quote_id = quote_data.get('id')
        if quote_id:
            items = quote_data.get('items', [])
            for i, item in enumerate(items):
                # If a quote item references its own quote_id as a product_id, that's suspicious
                if item.get('product_id') == quote_id:
                    issues.append(f"Potential circular reference: item[{i}] has product_id ({item.get('product_id')}) same as quote ID ({quote_id})")
        return issues

    def _check_schema_compatibility_enhanced(self) -> List[str]:
        """Compares the ideal schema (from file) with the actual live database schema."""
        issues = []

        if not self.ideal_schema:
            issues.append("Warning: No ideal schema provided to compare against. Only live database introspection is used.")
            return issues

        # Check for missing tables in live DB that are in ideal schema
        for table_name in self.ideal_schema.keys():
            if table_name not in self.live_db_schema:
                issues.append(f"Schema mismatch: Table '{table_name}' expected in ideal schema but not found in live database.")
            else:
                # Check for missing columns in live DB tables compared to ideal schema
                ideal_columns = set(self.ideal_schema[table_name].keys())
                live_columns = set(self.live_db_schema[table_name]['columns'])

                missing_live_cols = ideal_columns - live_columns
                for col in missing_live_cols:
                    # Ignore 'primary_key', 'auto_increment', 'foreign_key', 'description', 'unique' keys in ideal schema,
                    # as these are metadata about the column, not column names themselves.
                    # Also ignore properties like 'default' or 'nullable' which are attributes of a column, not the column itself.
                    if col not in ['primary_key', 'auto_increment', 'foreign_key', 'description', 'unique', 'default', 'nullable', 'name']:
                         issues.append(f"Schema mismatch: Column '{table_name}.{col}' expected in ideal schema but not found in live database.")

                # Check for extra columns in live DB that are not in ideal schema (could be harmless, but worth noting)
                extra_live_cols = live_columns - ideal_columns
                for col in extra_live_cols:
                    issues.append(f"Schema mismatch: Extra column '{table_name}.{col}' found in live database, not defined in ideal schema.")

                # Deeper check: Compare column types, nullability, etc., if detailed mismatch is desired
                for col_name, ideal_col_details in self.ideal_schema[table_name].items():
                    if col_name in self.live_db_schema[table_name]['column_details']:
                        live_col_details = self.live_db_schema[table_name]['column_details'][col_name]

                        # Compare types (simplistic string comparison)
                        ideal_type = str(ideal_col_details.get('type', 'UNKNOWN')).upper()
                        live_type = str(live_col_details.get('type', 'UNKNOWN')).upper()
                        # Be lenient with type names (e.g., VARCHAR vs VARCHAR(255) vs NVARCHAR, INTEGER vs INT)
                        if not (ideal_type in live_type or live_type in ideal_type):
                            issues.append(f"Schema mismatch: {table_name}.{col_name} type mismatch (Ideal: {ideal_type}, Live: {live_type})")

                        # Compare nullability
                        ideal_nullable = ideal_col_details.get('nullable', True)
                        live_nullable = live_col_details.get('nullable', True) # SQLAlchemy inspect uses 'nullable' key
                        if ideal_nullable != live_nullable:
                            issues.append(f"Schema mismatch: {table_name}.{col_name} nullability mismatch (Ideal: {'Nullable' if ideal_nullable else 'NOT NULL'}, Live: {'Nullable' if live_nullable else 'NOT NULL'})")

                        # Compare unique constraint presence (simplistic)
                        ideal_unique = ideal_col_details.get('unique', False)
                        # Live unique constraints are harder to get directly from column_details,
                        # would need to iterate inspector.get_unique_constraints(table_name)
                        # For now, just a basic check if ideal expects unique and live doesn't explicitly state it in details
                        if ideal_unique and not live_col_details.get('unique', False):
                            # This is a weak check. A proper check would inspect inspector.get_unique_constraints()
                            # For simplicity, if the live_db_schema's column_details doesn't explicitly state unique, it's a mismatch.
                            # More robust: check if (table, [col_name]) is in inspector.get_unique_constraints
                            pass # Skip for now as it needs more complex inspection comparison

        return issues


    def test_quote_save_enhanced(self, quote_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced quote save test with detailed error capture against the live database"""
        session = self.Session()
        result = {
            'success': False,
            'error_type': None,
            'error_message': '',
            'rollback_cause': '',
            'sql_statement': '',
            'parameters': {},
            'detailed_error': {}
        }

        try:
            # Build dynamic INSERT based on actual live DB schema to ensure it's runnable
            if 'quotes' not in self.live_db_schema:
                raise Exception("Quotes table not found in live database schema. Cannot perform save test.")

            available_columns = self.live_db_schema['quotes']['columns']
            # Filter quote_data to only include columns that exist in the actual DB table
            data_columns = [col for col in available_columns
                          if col in quote_data and col not in ['id', 'created_at', 'updated_at']]

            if not data_columns:
                raise Exception("No valid columns from quote_data found that match the live 'quotes' table schema for insertion.")

            # Build SQL dynamically
            columns_sql = ', '.join(data_columns)
            values_sql = ', '.join([f':{col}' for col in data_columns])

            quote_sql = f"""
                INSERT INTO quotes ({columns_sql})
                VALUES ({values_sql})
            """

            # Prepare parameters
            quote_params = {col: quote_data[col] for col in data_columns}

            result['sql_statement'] = quote_sql
            result['parameters'] = quote_params

            # Execute against the live database
            session.execute(text(quote_sql), quote_params)
            session.commit()
            result['success'] = True

        except IntegrityError as e:
            session.rollback()
            result['error_type'] = 'IntegrityError'
            result['error_message'] = str(e)
            result['rollback_cause'] = 'Database constraint violation (foreign key, unique, not null, check constraint)'
            result['detailed_error'] = self._parse_integrity_error(str(e))

        except StatementError as e:
            session.rollback()
            result['error_type'] = 'StatementError'
            result['error_message'] = str(e)
            result['rollback_cause'] = 'SQL statement error (syntax, data type mismatch in DB execution)'
            result['detailed_error'] = {'statement_error_orig': str(e.orig) if hasattr(e, 'orig') else str(e)}

        except DatabaseError as e:
            session.rollback()
            result['error_type'] = 'DatabaseError'
            result['error_message'] = str(e)
            result['rollback_cause'] = 'Database schema, connection, or operational issue'
            result['detailed_error'] = {'db_error_orig': str(e.orig) if hasattr(e, 'orig') else str(e)}

        except Exception as e:
            session.rollback()
            result['error_type'] = type(e).__name__
            result['error_message'] = str(e)
            result['rollback_cause'] = 'Unexpected error during save operation'
            result['detailed_error'] = {'traceback': traceback.format_exc()}

        finally:
            session.close()

        return result

    def _parse_integrity_error(self, error_msg: str) -> Dict[str, str]:
        """Parse integrity error message to identify specific constraint (DB specific parsing)"""
        error_info = {'constraint_type': 'unknown', 'constraint_name': '', 'details': error_msg}

        # Common patterns for different DBs
        error_msg_lower = error_msg.lower()

        # MySQL/MariaDB
        if 'duplicate entry' in error_msg_lower:
            error_info['constraint_type'] = 'unique'
            match = re.search(r"Duplicate entry '([^']+)' for key '([^']+)'", error_msg)
            if match:
                error_info['constraint_name'] = f"Key: {match.group(2)}, Value: {match.group(1)}"
            else:
                match = re.search(r"Duplicate entry '([^']+)'", error_msg)
                if match:
                    error_info['constraint_name'] = f"Value: {match.group(1)}"
        elif 'foreign key constraint fails' in error_msg_lower:
            error_info['constraint_type'] = 'foreign_key'
            match = re.search(r'CONSTRAINT `([^`]+)` FOREIGN KEY \(`([^`]+)`\)', error_msg)
            if match:
                error_info['constraint_name'] = f"Constraint: {match.group(1)}, Column: {match.group(2)}"
        elif 'cannot be null' in error_msg_lower or 'column \'([^\']+)\' cannot be null' in error_msg_lower:
            error_info['constraint_type'] = 'not_null'
            match = re.search(r'Column \'([^\']+)\' cannot be null', error_msg)
            if match:
                error_info['constraint_name'] = match.group(1)

        # PostgreSQL
        elif 'duplicate key value violates unique constraint' in error_msg_lower:
            error_info['constraint_type'] = 'unique'
            match = re.search(r'Key \(([^)]+)\)=\(([^)]+)\) already exists', error_msg)
            if match:
                error_info['constraint_name'] = f"Columns: {match.group(1)}, Value: {match.group(2)}"
        elif 'foreign key constraint' in error_msg_lower and 'violates' in error_msg_lower:
            error_info['constraint_type'] = 'foreign_key'
            match = re.search(r'Key \(([^)]+)\)=\(([^)]+)\) is not present in table "([^"]+)"', error_msg)
            if match:
                error_info['constraint_name'] = f"Column: {match.group(1)}, Value: {match.group(2)}, Table: {match.group(3)}"
        elif 'null value in column' in error_msg_lower and 'violates not-null constraint' in error_msg_lower:
            error_info['constraint_type'] = 'not_null'
            match = re.search(r'null value in column "([^"]+)"', error_msg)
            if match:
                error_info['constraint_name'] = match.group(1)

        # SQLite
        elif 'unique constraint failed' in error_msg_lower:
            error_info['constraint_type'] = 'unique'
            match = re.search(r'UNIQUE constraint failed: ([^\s]+)\.([^\s]+)', error_msg)
            if match:
                error_info['constraint_name'] = f"Table: {match.group(1)}, Column: {match.group(2)}"
        elif 'foreign key constraint failed' in error_msg_lower:
            error_info['constraint_type'] = 'foreign_key'
            error_info['constraint_name'] = 'Foreign Key Constraint' # SQLite generic message
        elif 'not null constraint failed' in error_msg_lower:
            error_info['constraint_type'] = 'not_null'
            match = re.search(r'NOT NULL constraint failed: ([^\s]+)\.([^\s]+)', error_msg)
            if match:
                error_info['constraint_name'] = f"Table: {match.group(1)}, Column: {match.group(2)}"

        return error_info

    def generate_fix_recommendations(self, issues: Dict[str, List[str]]) -> List[str]:
        """Generate actionable fix recommendations based on detected issues"""
        recommendations = []

        if sum(len(problems) for problems in issues.values()) == 0:
            recommendations.append("✨ No major issues detected. Looks good!")
            return recommendations

        # Critical fixes
        if issues['missing_required_fields']:
            recommendations.append("🔴 CRITICAL: Add missing required fields to your quote data")
            for issue in issues['missing_required_fields'][:3]:  # Show first 3
                recommendations.append(f"   → {issue}")
        
        if issues['foreign_key_violations']:
            recommendations.append("🔴 CRITICAL: Fix foreign key references")
            recommendations.append("   → Verify that referenced IDs exist in related tables (users, clients, products, statuses)")
            for issue in issues['foreign_key_violations'][:3]:
                recommendations.append(f"   → {issue}")

        if issues['data_type_issues']:
            recommendations.append("🔴 CRITICAL: Fix data type mismatches")
            recommendations.append("   → Ensure numeric fields contain valid numbers (e.g., '123.45', not 'abc')")
            recommendations.append("   → Verify date/datetime formats (e.g., 'YYYY-MM-DD', 'YYYY-MM-DD HH:MM:SS')")
            for issue in issues['data_type_issues'][:3]:
                recommendations.append(f"   → {issue}")

        # Warnings
        if issues['schema_mismatches']:
            recommendations.append("⚠️  WARNING: Address schema compatibility issues")
            recommendations.append("   → Your `quotes_schema.py` does not fully match the live database structure.")
            recommendations.append("   → This may indicate outdated documentation or an unexpected database change.")
            for issue in issues['schema_mismatches'][:3]:
                recommendations.append(f"   → {issue}")

        if issues['constraint_violations']:
            recommendations.append("⚠️  WARNING: Address other database constraint violations")
            if any('duplicate' in issue.lower() for issue in issues['constraint_violations']):
                recommendations.append("   → Use unique identifiers (e.g., unique `quote_number`)")
            if any('value too long' in issue.lower() for issue in issues['constraint_violations']):
                recommendations.append("   → Shorten string values to fit column length limits (e.g., `VARCHAR(255)`)")
            if any('negative value not allowed' in issue.lower() for issue in issues['constraint_violations']):
                recommendations.append("   → Ensure amounts, costs, quantities are non-negative")
            for issue in issues['constraint_violations'][:3]:
                recommendations.append(f"   → {issue}")

        if issues['business_logic_issues']:
            recommendations.append("⚠️  WARNING: Fix business logic issues")
            recommendations.append("   → Ensure `due_date` is after `quote_date`")
            recommendations.append("   → Verify `amount` calculations match item totals")
            recommendations.append("   → Ensure `balance` does not exceed `amount`")
            for issue in issues['business_logic_issues'][:3]:
                recommendations.append(f"   → {issue}")

        if issues['custom_field_issues']:
            recommendations.append("ℹ️  INFO: Check custom field data")
            recommendations.append("   → Ensure custom field names are valid and values fit length limits.")
            for issue in issues['custom_field_issues'][:3]:
                recommendations.append(f"   → {issue}")

        if issues['tax_rate_issues']:
            recommendations.append("ℹ️  INFO: Review tax rates")
            recommendations.append("   → Ensure tax rates are between 0 and 100.")
            for issue in issues['tax_rate_issues'][:3]:
                recommendations.append(f"   → {issue}")

        # General recommendations
        recommendations.extend([
            "",
            "💡 GENERAL RECOMMENDATIONS:",
            "   • Always validate foreign key references (users, clients, products, statuses) before submitting data.",
            "   • Use Decimal types for monetary values to avoid floating-point inaccuracies.",
            "   • Ensure date/datetime objects or correctly formatted strings are used for date fields.",
            "   • Regularly compare your `quotes_schema.py` with your live database schema for consistency.",
            "   • Check your database logs for more detailed error messages if the diagnostic is not specific enough."
        ])

        return recommendations

# Enhanced main diagnostic function
def diagnose_quote_migration_issues_enhanced(engine, session_factory, quote_data, verbose=True, ideal_schema: Dict[str, Any] = None):
    """Enhanced diagnostic with detailed reporting and fix recommendations"""
    if ideal_schema is None:
        ideal_schema = IDEAL_QUOTE_SCHEMA # Use the imported schema by default

    diagnostic = ImprovedQuoteRollbackDiagnostic(engine, session_factory, ideal_schema)

    if verbose:
        print("=== ENHANCED Quote Migration Rollback Diagnostic ===\n")
        print("NOTE: This diagnostic uses the provided IDEAL_QUOTE_SCHEMA (from file) for some checks,")
        print("      and also introspects the LIVE DATABASE schema for other checks and the save test.\n")

    # Run comprehensive diagnostics
    issues = diagnostic.diagnose_rollback_causes(quote_data)

    # Count total issues
    total_issues = sum(len(problems) for problems in issues.values())

    if verbose:
        # Display results with priorities
        critical_categories = ['missing_required_fields', 'foreign_key_
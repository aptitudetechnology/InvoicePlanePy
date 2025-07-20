import logging
import traceback
from decimal import Decimal, InvalidOperation
from datetime import datetime
from sqlalchemy import inspect, text, event
from sqlalchemy.exc import IntegrityError, DatabaseError, StatementError
from sqlalchemy.orm import sessionmaker
from typing import Dict, List, Any, Optional
import json
import re

class ImprovedQuoteRollbackDiagnostic:
    def __init__(self, engine, session_factory):
        self.engine = engine
        self.Session = session_factory
        self.logger = logging.getLogger(__name__)
        self.actual_schema = self._get_actual_schema()
        
    def _get_actual_schema(self) -> Dict[str, Any]:
        """Get actual database schema to avoid false positives"""
        inspector = inspect(self.engine)
        schema = {}
        
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            schema[table_name] = {
                'columns': [col['name'] for col in columns],
                'column_details': {col['name']: col for col in columns},
                'primary_keys': inspector.get_pk_constraint(table_name)['constrained_columns'],
                'foreign_keys': [fk for fk in inspector.get_foreign_keys(table_name)]
            }
        
        return schema
    
    def diagnose_rollback_causes(self, quote_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Enhanced diagnostic for quote rollback causes"""
        issues = {
            'missing_required_fields': [],
            'foreign_key_violations': [],
            'custom_field_issues': [],
            'tax_rate_issues': [],
            'constraint_violations': [],
            'schema_mismatches': [],
            'data_type_issues': [],
            'circular_dependencies': [],
            'transaction_issues': []
        }
        
        # Enhanced checks
        issues['missing_required_fields'] = self._check_required_fields_enhanced(quote_data)
        issues['foreign_key_violations'] = self._check_foreign_keys_enhanced(quote_data)
        issues['custom_field_issues'] = self._check_custom_fields(quote_data)
        issues['tax_rate_issues'] = self._check_tax_rates(quote_data)
        issues['constraint_violations'] = self._check_constraints_enhanced(quote_data)
        issues['schema_mismatches'] = self._check_schema_compatibility_enhanced()
        issues['data_type_issues'] = self._check_data_types(quote_data)
        issues['circular_dependencies'] = self._check_circular_dependencies(quote_data)
        
        return issues
    
    def _check_required_fields_enhanced(self, quote_data: Dict[str, Any]) -> List[str]:
        """Enhanced required fields check using actual schema"""
        issues = []
        
        # Check quotes table
        if 'quotes' in self.actual_schema:
            quote_columns = self.actual_schema['quotes']['column_details']
            for col_name, col_info in quote_columns.items():
                # Field is required if not nullable and no default
                if not col_info.get('nullable', True) and col_info.get('default') is None:
                    if col_name not in ['id', 'created_at', 'updated_at']:  # Skip auto-generated
                        if not quote_data.get(col_name):
                            issues.append(f"Missing required quote field: {col_name}")
        
        # Check quote_items if present
        items = quote_data.get('items', [])
        if items and 'quote_items' in self.actual_schema:
            item_columns = self.actual_schema['quote_items']['column_details']
            for i, item in enumerate(items):
                for col_name, col_info in item_columns.items():
                    if not col_info.get('nullable', True) and col_info.get('default') is None:
                        if col_name not in ['id', 'quote_id', 'created_at', 'updated_at']:
                            if not item.get(col_name):
                                issues.append(f"Missing required field '{col_name}' in item {i}")
        
        return issues
    
    def _check_foreign_keys_enhanced(self, quote_data: Dict[str, Any]) -> List[str]:
        """Enhanced foreign key check with batch validation"""
        issues = []
        session = self.Session()
        
        try:
            # Collect all foreign key checks to batch them
            fk_checks = []
            
            # Check quote foreign keys
            if 'quotes' in self.actual_schema:
                for fk in self.actual_schema['quotes']['foreign_keys']:
                    col_name = fk['constrained_columns'][0]
                    ref_table = fk['referred_table']
                    ref_col = fk['referred_columns'][0]
                    
                    if quote_data.get(col_name):
                        fk_checks.append({
                            'value': quote_data[col_name],
                            'table': ref_table,
                            'column': ref_col,
                            'source': f'quote.{col_name}'
                        })
            
            # Check item foreign keys
            items = quote_data.get('items', [])
            if items and 'quote_items' in self.actual_schema:
                for i, item in enumerate(items):
                    for fk in self.actual_schema['quote_items']['foreign_keys']:
                        col_name = fk['constrained_columns'][0]
                        ref_table = fk['referred_table']
                        ref_col = fk['referred_columns'][0]
                        
                        if item.get(col_name):
                            fk_checks.append({
                                'value': item[col_name],
                                'table': ref_table,
                                'column': ref_col,
                                'source': f'item[{i}].{col_name}'
                            })
            
            # Batch validate foreign keys
            for check in fk_checks:
                try:
                    result = session.execute(
                        text(f"SELECT 1 FROM {check['table']} WHERE {check['column']} = :value LIMIT 1"),
                        {'value': check['value']}
                    ).fetchone()
                    
                    if not result:
                        issues.append(f"Foreign key violation: {check['source']} = {check['value']} not found in {check['table']}.{check['column']}")
                except Exception as e:
                    issues.append(f"Error checking foreign key {check['source']}: {str(e)}")
        
        except Exception as e:
            issues.append(f"Error in foreign key validation: {str(e)}")
        finally:
            session.close()
        
        return issues
    
    def _check_data_types(self, quote_data: Dict[str, Any]) -> List[str]:
        """Check for data type mismatches that could cause rollbacks"""
        issues = []
        
        def validate_field_type(value, expected_type, field_name):
            if value is None:
                return True
            
            try:
                if 'INT' in expected_type.upper():
                    int(value)
                elif 'DECIMAL' in expected_type.upper() or 'NUMERIC' in expected_type.upper():
                    Decimal(str(value))
                elif 'FLOAT' in expected_type.upper() or 'DOUBLE' in expected_type.upper():
                    float(value)
                elif 'DATE' in expected_type.upper():
                    if isinstance(value, str):
                        # Basic date format validation
                        if not re.match(r'\d{4}-\d{2}-\d{2}', value):
                            return False
                elif 'TIMESTAMP' in expected_type.upper() or 'DATETIME' in expected_type.upper():
                    if isinstance(value, str):
                        if not re.match(r'\d{4}-\d{2}-\d{2}[\s|T]\d{2}:\d{2}:\d{2}', value):
                            return False
                return True
            except (ValueError, InvalidOperation, TypeError):
                return False
        
        # Check quote data types
        if 'quotes' in self.actual_schema:
            for field_name, value in quote_data.items():
                if field_name in self.actual_schema['quotes']['column_details']:
                    col_type = str(self.actual_schema['quotes']['column_details'][field_name]['type'])
                    if not validate_field_type(value, col_type, field_name):
                        issues.append(f"Data type mismatch for quote.{field_name}: {value} (expected {col_type})")
        
        # Check item data types
        items = quote_data.get('items', [])
        if items and 'quote_items' in self.actual_schema:
            for i, item in enumerate(items):
                for field_name, value in item.items():
                    if field_name in self.actual_schema['quote_items']['column_details']:
                        col_type = str(self.actual_schema['quote_items']['column_details'][field_name]['type'])
                        if not validate_field_type(value, col_type, field_name):
                            issues.append(f"Data type mismatch for item[{i}].{field_name}: {value} (expected {col_type})")
        
        return issues
    
    def _check_constraints_enhanced(self, quote_data: Dict[str, Any]) -> List[str]:
        """Enhanced constraint checking"""
        issues = []
        session = self.Session()
        
        try:
            # Check unique constraints
            if 'quotes' in self.actual_schema and quote_data.get('quote_number'):
                # More sophisticated duplicate check
                query = text("""
                    SELECT id, quote_number FROM quotes 
                    WHERE quote_number = :quote_number
                    AND (:quote_id IS NULL OR id != :quote_id)
                """)
                
                result = session.execute(query, {
                    'quote_number': quote_data['quote_number'],
                    'quote_id': quote_data.get('id')
                }).fetchone()
                
                if result:
                    issues.append(f"Duplicate quote_number: {quote_data['quote_number']} already exists (ID: {result[0]})")
            
            # Check string length constraints
            if 'quotes' in self.actual_schema:
                for field_name, value in quote_data.items():
                    if isinstance(value, str) and field_name in self.actual_schema['quotes']['column_details']:
                        col_info = self.actual_schema['quotes']['column_details'][field_name]
                        col_type = str(col_info['type'])
                        
                        # Extract length from VARCHAR(n) or CHAR(n)
                        if 'VARCHAR' in col_type or 'CHAR' in col_type:
                            match = re.search(r'\((\d+)\)', col_type)
                            if match:
                                max_length = int(match.group(1))
                                if len(value) > max_length:
                                    issues.append(f"Value too long for {field_name}: {len(value)} chars > {max_length} max")
            
            # Check numeric ranges
            numeric_fields = ['amount', 'balance', 'partial', 'cost', 'qty', 'tax_rate']
            for field in numeric_fields:
                if field in quote_data:
                    try:
                        val = float(quote_data[field])
                        if val < 0 and field in ['amount', 'balance', 'cost', 'qty']:
                            issues.append(f"Negative value not allowed for {field}: {val}")
                        if field == 'tax_rate' and (val < 0 or val > 100):
                            issues.append(f"Tax rate out of range (0-100): {val}")
                    except (ValueError, TypeError):
                        issues.append(f"Invalid numeric value for {field}: {quote_data[field]}")
            
            # Check items numeric constraints
            items = quote_data.get('items', [])
            for i, item in enumerate(items):
                for field in ['cost', 'qty', 'tax_rate']:
                    if field in item:
                        try:
                            val = float(item[field])
                            if val < 0 and field in ['cost', 'qty']:
                                issues.append(f"Negative value not allowed for item[{i}].{field}: {val}")
                        except (ValueError, TypeError):
                            issues.append(f"Invalid numeric value for item[{i}].{field}: {item[field]}")
        
        except Exception as e:
            issues.append(f"Error checking constraints: {str(e)}")
        finally:
            session.close()
        
        return issues
    
    def _check_circular_dependencies(self, quote_data: Dict[str, Any]) -> List[str]:
        """Check for circular dependency issues"""
        issues = []
        
        # Check if quote references itself
        quote_id = quote_data.get('id')
        if quote_id:
            items = quote_data.get('items', [])
            for i, item in enumerate(items):
                if item.get('quote_id') == quote_id and item.get('product_id') == quote_id:
                    issues.append(f"Potential circular reference in item[{i}]")
        
        return issues
    
    def _check_schema_compatibility_enhanced(self) -> List[str]:
        """Enhanced schema compatibility check"""
        issues = []
        
        required_tables = ['quotes']
        optional_tables = ['quote_items', 'quote_custom_fields', 'quote_tax_rates']
        
        # Check required tables
        for table in required_tables:
            if table not in self.actual_schema:
                issues.append(f"Required table missing: {table}")
        
        # Warn about optional tables
        for table in optional_tables:
            if table not in self.actual_schema:
                issues.append(f"Optional table missing (may limit functionality): {table}")
        
        return issues
    
    def test_quote_save_enhanced(self, quote_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced quote save test with detailed error capture"""
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
            # Build dynamic INSERT based on actual schema
            if 'quotes' not in self.actual_schema:
                raise Exception("Quotes table not found in schema")
            
            available_columns = self.actual_schema['quotes']['columns']
            data_columns = [col for col in available_columns 
                          if col in quote_data and col not in ['id', 'created_at', 'updated_at']]
            
            if not data_columns:
                raise Exception("No valid columns found in quote data")
            
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
            
            # Execute
            session.execute(text(quote_sql), quote_params)
            session.commit()
            result['success'] = True
            
        except IntegrityError as e:
            session.rollback()
            result['error_type'] = 'IntegrityError'
            result['error_message'] = str(e)
            result['rollback_cause'] = 'Database constraint violation (foreign key, unique, not null)'
            result['detailed_error'] = self._parse_integrity_error(str(e))
            
        except StatementError as e:
            session.rollback()
            result['error_type'] = 'StatementError'
            result['error_message'] = str(e)
            result['rollback_cause'] = 'SQL statement error (syntax, data type mismatch)'
            result['detailed_error'] = {'statement_error': str(e.orig) if hasattr(e, 'orig') else str(e)}
            
        except DatabaseError as e:
            session.rollback()
            result['error_type'] = 'DatabaseError'
            result['error_message'] = str(e)
            result['rollback_cause'] = 'Database schema or connection issue'
            
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
        """Parse integrity error message to identify specific constraint"""
        error_info = {'constraint_type': 'unknown', 'constraint_name': '', 'details': error_msg}
        
        if 'foreign key constraint' in error_msg.lower():
            error_info['constraint_type'] = 'foreign_key'
            # Try to extract table/column info
            fk_match = re.search(r'FOREIGN KEY.*?`([^`]+)`.*?REFERENCES.*?`([^`]+)`', error_msg)
            if fk_match:
                error_info['constraint_name'] = f"{fk_match.group(1)} -> {fk_match.group(2)}"
        
        elif 'unique constraint' in error_msg.lower() or 'duplicate entry' in error_msg.lower():
            error_info['constraint_type'] = 'unique'
            unique_match = re.search(r"Duplicate entry '([^']+)'", error_msg)
            if unique_match:
                error_info['constraint_name'] = unique_match.group(1)
        
        elif 'not null constraint' in error_msg.lower():
            error_info['constraint_type'] = 'not_null'
            null_match = re.search(r'Column \'([^\']+)\'', error_msg)
            if null_match:
                error_info['constraint_name'] = null_match.group(1)
        
        return error_info

# Enhanced main diagnostic function
def diagnose_quote_migration_issues_enhanced(engine, session_factory, quote_data, verbose=True):
    """Enhanced diagnostic with detailed reporting"""
    diagnostic = ImprovedQuoteRollbackDiagnostic(engine, session_factory)
    
    if verbose:
        print("=== ENHANCED Quote Migration Rollback Diagnostic ===\n")
    
    # Run comprehensive diagnostics
    issues = diagnostic.diagnose_rollback_causes(quote_data)
    
    # Count total issues
    total_issues = sum(len(problems) for problems in issues.values())
    
    if verbose:
        # Display results with priorities
        critical_categories = ['missing_required_fields', 'foreign_key_violations', 'data_type_issues']
        warning_categories = ['schema_mismatches', 'constraint_violations']
        
        print(f"TOTAL ISSUES FOUND: {total_issues}\n")
        
        # Show critical issues first
        for category in critical_categories:
            problems = issues.get(category, [])
            if problems:
                print(f"🚨 CRITICAL - {category.upper().replace('_', ' ')}:")
                for problem in problems:
                    print(f"   ❌ {problem}")
                print()
        
        # Show warnings
        for category in warning_categories:
            problems = issues.get(category, [])
            if problems:
                print(f"⚠️  WARNING - {category.upper().replace('_', ' ')}:")
                for problem in problems:
                    print(f"   ⚠️  {problem}")
                print()
        
        # Show other issues
        other_categories = [cat for cat in issues.keys() 
                          if cat not in critical_categories + warning_categories]
        for category in other_categories:
            problems = issues.get(category, [])
            if problems:
                print(f"ℹ️  INFO - {category.upper().replace('_', ' ')}:")
                for problem in problems:
                    print(f"   ℹ️  {problem}")
                print()
    
    # Test actual save operation with enhanced error reporting
    if verbose:
        print("=" * 50)
        print("TESTING ACTUAL SAVE OPERATION:")
        print("=" * 50)
    
    save_result = diagnostic.test_quote_save_enhanced(quote_data)
    
    if save_result['success']:
        if verbose:
            print("✅ Quote save test PASSED")
    else:
        if verbose:
            print("❌ Quote save test FAILED")
            print(f"   Error Type: {save_result['error_type']}")
            print(f"   Rollback Cause: {save_result['rollback_cause']}")
            print(f"   Error Message: {save_result['error_message']}")
            
            if save_result.get('detailed_error'):
                print(f"   Detailed Error: {save_result['detailed_error']}")
            
            if save_result.get('sql_statement'):
                print(f"   SQL Statement: {save_result['sql_statement']}")
                print(f"   Parameters: {save_result['parameters']}")
    
    return issues, save_result

# Usage example with better test data
if __name__ == "__main__":
    # More realistic test data
    test_quote_data = {
        'user_id': 1,
        'client_id': 123,
        'quote_number': 'Q-2024-001',
        'quote_date': '2024-01-15',
        'due_date': '2024-02-15',
        'amount': 1500.00,
        'balance': 1500.00,
        'status_id': 1,
        'items': [
            {
                'product_id': 456,
                'notes': 'Web development services',
                'cost': 750.00,
                'qty': 2,
                'tax_rate': 20.0
            }
        ]
    }
    
    print("Example usage:")
    print("from your_app import engine, Session")
    print("issues, save_result = diagnose_quote_migration_issues_enhanced(engine, Session, test_quote_data)")
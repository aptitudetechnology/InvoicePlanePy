import logging
import traceback
from decimal import Decimal, InvalidOperation
from datetime import datetime
from sqlalchemy import inspect, text, event, create_engine
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
        
        try:
            for table_name in inspector.get_table_names():
                columns = inspector.get_columns(table_name)
                schema[table_name] = {
                    'columns': [col['name'] for col in columns],
                    'column_details': {col['name']: col for col in columns},
                    'primary_keys': inspector.get_pk_constraint(table_name)['constrained_columns'],
                    'foreign_keys': [fk for fk in inspector.get_foreign_keys(table_name)]
                }
        except Exception as e:
            self.logger.error(f"Error retrieving schema: {str(e)}")
        
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
            'transaction_issues': [],
            'business_logic_issues': []
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
        issues['business_logic_issues'] = self._check_business_logic(quote_data)
        
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
    
    def _check_custom_fields(self, quote_data: Dict[str, Any]) -> List[str]:
        """Check custom field issues"""
        issues = []
        custom_fields = quote_data.get('custom_fields', {})
        
        if custom_fields:
            if 'quote_custom_fields' not in self.actual_schema:
                issues.append("Custom fields data provided but quote_custom_fields table not found")
            else:
                # Validate custom field structure
                for field_name, field_value in custom_fields.items():
                    if not isinstance(field_name, str) or len(field_name.strip()) == 0:
                        issues.append(f"Invalid custom field name: {field_name}")
                    
                    # Check field value length if string
                    if isinstance(field_value, str) and len(field_value) > 1000:
                        issues.append(f"Custom field value too long for {field_name}: {len(field_value)} chars")
        
        return issues
    
    def _check_tax_rates(self, quote_data: Dict[str, Any]) -> List[str]:
        """Check tax rate related issues"""
        issues = []
        
        # Check main quote tax rate
        if 'tax_rate' in quote_data:
            try:
                tax_rate = float(quote_data['tax_rate'])
                if tax_rate < 0 or tax_rate > 100:
                    issues.append(f"Quote tax rate out of range (0-100): {tax_rate}")
            except (ValueError, TypeError):
                issues.append(f"Invalid tax rate format: {quote_data['tax_rate']}")
        
        # Check item tax rates
        items = quote_data.get('items', [])
        for i, item in enumerate(items):
            if 'tax_rate' in item:
                try:
                    tax_rate = float(item['tax_rate'])
                    if tax_rate < 0 or tax_rate > 100:
                        issues.append(f"Item[{i}] tax rate out of range (0-100): {tax_rate}")
                except (ValueError, TypeError):
                    issues.append(f"Invalid tax rate format for item[{i}]: {item['tax_rate']}")
        
        return issues
    
    def _check_business_logic(self, quote_data: Dict[str, Any]) -> List[str]:
        """Check business logic constraints"""
        issues = []
        
        # Check date logic
        quote_date = quote_data.get('quote_date')
        due_date = quote_data.get('due_date')
        
        if quote_date and due_date:
            try:
                q_date = datetime.strptime(quote_date, '%Y-%m-%d') if isinstance(quote_date, str) else quote_date
                d_date = datetime.strptime(due_date, '%Y-%m-%d') if isinstance(due_date, str) else due_date
                
                if d_date < q_date:
                    issues.append(f"Due date ({due_date}) cannot be before quote date ({quote_date})")
            except ValueError:
                issues.append("Invalid date format in quote_date or due_date")
        
        # Check amount calculations
        items = quote_data.get('items', [])
        if items:
            calculated_total = 0
            for item in items:
                try:
                    cost = float(item.get('cost', 0))
                    qty = float(item.get('qty', 1))
                    calculated_total += cost * qty
                except (ValueError, TypeError):
                    issues.append(f"Invalid numeric values in item calculation")
            
            quote_amount = quote_data.get('amount')
            if quote_amount:
                try:
                    amount_diff = abs(float(quote_amount) - calculated_total)
                    if amount_diff > 0.01:  # Allow for small rounding differences
                        issues.append(f"Quote amount ({quote_amount}) doesn't match calculated total ({calculated_total:.2f})")
                except (ValueError, TypeError):
                    pass
        
        # Check balance logic
        amount = quote_data.get('amount')
        balance = quote_data.get('balance')
        if amount and balance:
            try:
                if float(balance) > float(amount):
                    issues.append(f"Balance ({balance}) cannot exceed amount ({amount})")
            except (ValueError, TypeError):
                pass
        
        return issues
    
    def _check_data_types(self, quote_data: Dict[str, Any]) -> List[str]:
        """Check for data type mismatches that could cause rollbacks"""
        issues = []
        
        def validate_field_type(value, expected_type, field_name):
            if value is None:
                return True
            
            try:
                type_upper = expected_type.upper()
                if any(t in type_upper for t in ['INT', 'INTEGER']):
                    int(value)
                elif any(t in type_upper for t in ['DECIMAL', 'NUMERIC']):
                    Decimal(str(value))
                elif any(t in type_upper for t in ['FLOAT', 'DOUBLE', 'REAL']):
                    float(value)
                elif 'DATE' in type_upper and 'TIME' not in type_upper:
                    if isinstance(value, str):
                        if not re.match(r'\d{4}-\d{2}-\d{2}', value):
                            return False
                elif any(t in type_upper for t in ['TIMESTAMP', 'DATETIME']):
                    if isinstance(value, str):
                        if not re.match(r'\d{4}-\d{2}-\d{2}[\s|T]\d{2}:\d{2}:\d{2}', value):
                            return False
                elif any(t in type_upper for t in ['VARCHAR', 'CHAR', 'TEXT']):
                    if not isinstance(value, (str, type(None))):
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

    def generate_fix_recommendations(self, issues: Dict[str, List[str]]) -> List[str]:
        """Generate actionable fix recommendations based on detected issues"""
        recommendations = []
        
        # Critical fixes
        if issues['missing_required_fields']:
            recommendations.append("🔴 CRITICAL: Add missing required fields to your quote data")
            for issue in issues['missing_required_fields'][:3]:  # Show first 3
                recommendations.append(f"   → {issue}")
        
        if issues['foreign_key_violations']:
            recommendations.append("🔴 CRITICAL: Fix foreign key references")
            recommendations.append("   → Verify that referenced IDs exist in related tables")
            recommendations.append("   → Check user_id, client_id, product_id values")
        
        if issues['data_type_issues']:
            recommendations.append("🔴 CRITICAL: Fix data type mismatches")
            recommendations.append("   → Ensure numeric fields contain valid numbers")
            recommendations.append("   → Verify date formats (YYYY-MM-DD)")
        
        # Warnings
        if issues['constraint_violations']:
            recommendations.append("⚠️  WARNING: Address constraint violations")
            if any('duplicate' in issue.lower() for issue in issues['constraint_violations']):
                recommendations.append("   → Use unique quote numbers")
        
        if issues['business_logic_issues']:
            recommendations.append("⚠️  WARNING: Fix business logic issues")
            recommendations.append("   → Ensure due date is after quote date")
            recommendations.append("   → Verify amount calculations match item totals")
        
        # General recommendations
        recommendations.extend([
            "",
            "💡 GENERAL RECOMMENDATIONS:",
            "   • Test with a minimal quote first (required fields only)",
            "   • Validate all foreign key references before saving",
            "   • Use proper data types (Decimal for money, datetime for dates)",
            "   • Check database logs for detailed error messages"
        ])
        
        return recommendations

# Enhanced main diagnostic function
def diagnose_quote_migration_issues_enhanced(engine, session_factory, quote_data, verbose=True):
    """Enhanced diagnostic with detailed reporting and fix recommendations"""
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
        warning_categories = ['schema_mismatches', 'constraint_violations', 'business_logic_issues']
        
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
        print("=" * 60)
        print("TESTING ACTUAL SAVE OPERATION:")
        print("=" * 60)
    
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
    
    # Generate and show fix recommendations
    if verbose and total_issues > 0:
        print("\n" + "=" * 60)
        print("FIX RECOMMENDATIONS:")
        print("=" * 60)
        recommendations = diagnostic.generate_fix_recommendations(issues)
        for rec in recommendations:
            print(rec)
    
    return issues, save_result

# Demo function to show how to use the diagnostic
def demo_usage():
    """Demonstrate how to use the diagnostic tool"""
    print("DEMO: How to use the Quote Rollback Diagnostic Tool")
    print("=" * 60)
    
    # Example database setup (you'll need to replace this with your actual setup)
    print("""
# 1. Set up your database connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your actual database URL
DATABASE_URL = "mysql://user:password@localhost/your_db"
# or
DATABASE_URL = "postgresql://user:password@localhost/your_db" 
# or
DATABASE_URL = "sqlite:///path/to/your/db.sqlite"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
""")
    
    # Example usage
    print("""
# 2. Prepare your quote data for testing
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

# 3. Run the diagnostic
issues, save_result = diagnose_quote_migration_issues_enhanced(
    engine, Session, test_quote_data, verbose=True
)

# 4. Analyze results
if save_result['success']:
    print("✅ Quote would save successfully!")
else:
    print("❌ Quote save would fail:")
    print(f"Error: {save_result['error_message']}")
    
    # Fix issues and try again
    # ... make corrections based on recommendations
    # Re-run diagnostic
""")

# Utility function to create a test database connection
def create_test_connection(database_url=None):
    """Create a test database connection - replace with your actual connection"""
    if database_url is None:
        # Example SQLite connection for testing
        database_url = "sqlite:///test_quotes.db"
        print(f"Using test database: {database_url}")
        print("⚠️  Replace with your actual database connection!")
    
    try:
        engine = create_engine(database_url, echo=False)
        Session = sessionmaker(bind=engine)
        return engine, Session
    except Exception as e:
        print(f"❌ Failed to create database connection: {e}")
        return None, None

# Main execution
if __name__ == "__main__":
    demo_usage()
    
    print("\n" + "=" * 60)
    print("RUNNING EXAMPLE DIAGNOSTIC:")
    print("=" * 60)
    
    # More realistic test data with potential issues
    test_quote_data_with_issues = {
        'user_id': 1,
        'client_id': 123,
        'quote_number': 'Q-2024-001',
        'quote_date': '2024-01-15',
        'due_date': '2024-01-10',  # Issue: due date before quote date
        'amount': 1500.00,
        'balance': 2000.00,  # Issue: balance exceeds amount
        'status_id': 1,
        'notes': 'A' * 1000,  # Potentially too long
        'items': [
            {
                'product_id': 999999,  # Issue: likely doesn't exist
                'notes': 'Web development services',
                'cost': -100.00,  # Issue: negative cost
                'qty': 2,
                'tax_rate': 150.0  # Issue: tax rate > 100%
            },
            {
                'product_id': 456,
                'notes': '',  # Potentially missing required field
                'cost': 750.00,
                'qty': 0,  # Issue: zero quantity
                'tax_rate': 20.0
            }
        ]
    }
    
    test_quote_data_clean = {
        'user_id': 1,
        'client_id': 123,
        'quote_number': 'Q-2024-002',
        'quote_date': '2024-01-15',
        'due_date': '2024-02-15',
        'amount': 1650.00,
        'balance': 1650.00,
        'status_id': 1,
        'notes': 'Clean quote for testing',
        'items': [
            {
                'product_id': 456,
                'notes': 'Web development services',
                'cost': 750.00,
                'qty': 2,
                'tax_rate': 10.0
            }
        ]
    }
    
    print("Testing with PROBLEMATIC quote data:")
    print("=" * 40)
    
    # This would normally use your actual database connection
    # For demo purposes, we'll show what the output would look like
    try:
        # Uncomment and modify these lines with your actual database connection:
        # engine, Session = create_test_connection("your_database_url_here")
        # if engine and Session:
        #     issues, save_result = diagnose_quote_migration_issues_enhanced(
        #         engine, Session, test_quote_data_with_issues, verbose=True
        #     )
        
        print("💡 To run this diagnostic with your database:")
        print("   1. Replace the database connection with your actual connection")
        print("   2. Ensure your quote tables exist in the database") 
        print("   3. Run: python quote_diagnostic.py")
        print()
        
        # Show what issues would be found
        print("Expected issues in the test data:")
        print("🚨 CRITICAL Issues:")
        print("   ❌ Foreign key violation: product_id 999999 likely doesn't exist")
        print("   ❌ Data type issue: negative cost value (-100.00)")
        print()
        print("⚠️  WARNING Issues:")
        print("   ⚠️  Business logic: due date (2024-01-10) before quote date (2024-01-15)")
        print("   ⚠️  Business logic: balance (2000.00) exceeds amount (1500.00)")
        print("   ⚠️  Constraint violation: tax rate out of range (150.0%)")
        print("   ⚠️  Business logic: zero quantity in item")
        print()
        
        print("Testing with CLEAN quote data:")
        print("=" * 40)
        print("✅ Clean data should pass all validations")
        
    except Exception as e:
        print(f"Demo error: {e}")
    
    print("\n" + "=" * 60)
    print("INTEGRATION INSTRUCTIONS:")
    print("=" * 60)
    print("""
To integrate this diagnostic tool into your application:

1. SETUP:
   from quote_diagnostic import diagnose_quote_migration_issues_enhanced
   
2. BEFORE SAVING A QUOTE:
   issues, save_result = diagnose_quote_migration_issues_enhanced(
       engine, Session, quote_data, verbose=False
   )
   
   if not save_result['success']:
       # Handle the error
       logger.error(f"Quote save would fail: {save_result['error_message']}")
       return {"error": save_result['rollback_cause']}
   
3. DURING DEVELOPMENT/DEBUGGING:
   # Run with verbose=True to see detailed output
   issues, save_result = diagnose_quote_migration_issues_enhanced(
       engine, Session, quote_data, verbose=True
   )

4. AUTOMATED TESTING:
   # Use in unit tests to verify quote data integrity
   def test_quote_data_validity():
       issues, save_result = diagnose_quote_migration_issues_enhanced(
           engine, Session, test_quote_data
       )
       assert save_result['success'], f"Quote validation failed: {save_result['error_message']}"

5. MONITORING:
   # Log issues for monitoring quote save problems
   total_issues = sum(len(problems) for problems in issues.values())
   if total_issues > 0:
       logger.warning(f"Quote has {total_issues} validation issues")
""")

    print("\n🎯 NEXT STEPS:")
    print("1. Replace the database connection with your actual connection")
    print("2. Run this script with your real quote data")
    print("3. Fix any issues identified by the diagnostic")
    print("4. Integrate the diagnostic into your quote save workflow")
    print("5. Use the recommendations to prevent future rollback issues")
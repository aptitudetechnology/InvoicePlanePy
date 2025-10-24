#!/usr/bin/env python3
"""
SQLAlchemy Model Testing Script
This script tests SQLAlchemy models for common issues like:
- Missing imports
- Circular dependencies
- Invalid relationships
- Table creation
- Basic CRUD operations
"""

import sys
import traceback
from contextlib import contextmanager
from sqlalchemy import create_engine, inspect, MetaData, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTester:
    def __init__(self, database_url="sqlite:///:memory:"):
        """Initialize the model tester with a database URL."""
        self.database_url = database_url
        self.engine = None
        self.Session = None
        self.models = {}
        self.issues = []
        
    def setup_database(self):
        """Set up the database connection."""
        try:
            self.engine = create_engine(
                self.database_url, 
                echo=False,  # Set to True for SQL debugging
                pool_pre_ping=True
            )
            self.Session = sessionmaker(bind=self.engine)
            logger.info(f"✅ Database connection established: {self.database_url}")
            return True
        except Exception as e:
            self.issues.append(f"❌ Database connection failed: {e}")
            logger.error(f"Database connection failed: {e}")
            return False
    
    @contextmanager
    def get_session(self):
        """Context manager for database sessions."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def discover_models(self, base_class):
        """Discover all models from a declarative base."""
        try:
            self.models = {
                cls.__name__: cls 
                for cls in base_class.registry._class_registry.values()
                if hasattr(cls, '__tablename__')
            }
            logger.info(f"✅ Discovered {len(self.models)} models: {list(self.models.keys())}")
            return True
        except Exception as e:
            self.issues.append(f"❌ Model discovery failed: {e}")
            logger.error(f"Model discovery failed: {e}")
            return False
    
    def test_model_imports(self):
        """Test if all models can be imported without errors."""
        logger.info("🔍 Testing model imports...")
        
        for model_name, model_class in self.models.items():
            try:
                # Try to access the model's metadata
                _ = model_class.__table__
                logger.info(f"✅ {model_name}: Import successful")
            except Exception as e:
                self.issues.append(f"❌ {model_name}: Import failed - {e}")
                logger.error(f"❌ {model_name}: Import failed - {e}")
    
    def test_model_relationships(self):
        """Test model relationships for common issues."""
        logger.info("🔍 Testing model relationships...")
        
        for model_name, model_class in self.models.items():
            try:
                # Force relationship configuration
                model_class.__mapper__.configure()
                
                # Check each relationship
                for rel_name, rel_obj in model_class.__mapper__.relationships.items():
                    try:
                        # Try to access the related model
                        related_model = rel_obj.mapper.class_
                        logger.info(f"✅ {model_name}.{rel_name} -> {related_model.__name__}")
                    except Exception as e:
                        self.issues.append(f"❌ {model_name}.{rel_name}: Relationship error - {e}")
                        logger.error(f"❌ {model_name}.{rel_name}: Relationship error - {e}")
                        
            except Exception as e:
                self.issues.append(f"❌ {model_name}: Relationship configuration failed - {e}")
                logger.error(f"❌ {model_name}: Relationship configuration failed - {e}")
    
    def test_table_creation(self):
        """Test if tables can be created successfully."""
        logger.info("🔍 Testing table creation...")
        
        try:
            # Get the metadata from the models
            metadata = MetaData()
            for model_class in self.models.values():
                model_class.__table__.tometadata(metadata)
            
            # Create all tables
            metadata.create_all(self.engine)
            logger.info("✅ All tables created successfully")
            
            # Verify tables exist
            inspector = inspect(self.engine)
            created_tables = inspector.get_table_names()
            logger.info(f"✅ Created tables: {created_tables}")
            
            return True
            
        except Exception as e:
            self.issues.append(f"❌ Table creation failed: {e}")
            logger.error(f"❌ Table creation failed: {e}")
            return False
    
    def test_basic_crud(self):
        """Test basic CRUD operations on models."""
        logger.info("🔍 Testing basic CRUD operations...")
        
        for model_name, model_class in self.models.items():
            try:
                with self.get_session() as session:
                    # Test querying (should not fail even if table is empty)
                    query_result = session.query(model_class).first()
                    logger.info(f"✅ {model_name}: Query successful (result: {query_result})")
                    
                    # Test counting
                    count = session.query(model_class).count()
                    logger.info(f"✅ {model_name}: Count successful ({count} records)")
                    
            except Exception as e:
                self.issues.append(f"❌ {model_name}: CRUD test failed - {e}")
                logger.error(f"❌ {model_name}: CRUD test failed - {e}")
    
    def test_foreign_keys(self):
        """Test foreign key constraints."""
        logger.info("🔍 Testing foreign key constraints...")
        
        inspector = inspect(self.engine)
        
        for model_name, model_class in self.models.items():
            try:
                table_name = model_class.__tablename__
                foreign_keys = inspector.get_foreign_keys(table_name)
                
                if foreign_keys:
                    logger.info(f"✅ {model_name}: Foreign keys found: {len(foreign_keys)}")
                    for fk in foreign_keys:
                        logger.info(f"   - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
                else:
                    logger.info(f"ℹ️  {model_name}: No foreign keys")
                    
            except Exception as e:
                self.issues.append(f"❌ {model_name}: Foreign key inspection failed - {e}")
                logger.error(f"❌ {model_name}: Foreign key inspection failed - {e}")
    
    def check_common_issues(self):
        """Check for common SQLAlchemy issues."""
        logger.info("🔍 Checking for common issues...")
        
        # Check for circular imports and missing model references
        for model_name, model_class in self.models.items():
            try:
                # Check if model has relationships with string references
                for rel_name, rel_obj in model_class.__mapper__.relationships.items():
                    if hasattr(rel_obj, 'argument') and isinstance(rel_obj.argument, str):
                        referenced_model = rel_obj.argument
                        if referenced_model not in self.models:
                            self.issues.append(f"⚠️  {model_name}.{rel_name}: References unknown model '{referenced_model}'")
                            logger.warning(f"⚠️  {model_name}.{rel_name}: References unknown model '{referenced_model}'")
                        else:
                            logger.info(f"✅ {model_name}.{rel_name}: String reference '{referenced_model}' resolved")
                
                # Specific check for common missing models in InvoicePlane
                if model_name == "User":
                    # Check if User has problematic Quote relationship
                    user_rels = [rel.argument for rel in model_class.__mapper__.relationships.values() 
                                if hasattr(rel, 'argument') and isinstance(rel.argument, str)]
                    if "Quote" in user_rels:
                        self.issues.append(f"❌ {model_name}: Still has Quote relationship - should be commented out")
                        logger.error(f"❌ {model_name}: Still has Quote relationship - should be commented out")
                    else:
                        logger.info(f"✅ {model_name}: Quote relationship properly removed/commented")
                
                if model_name == "Client":
                    # Check if Client has problematic relationships
                    client_rels = [rel.argument for rel in model_class.__mapper__.relationships.values() 
                                 if hasattr(rel, 'argument') and isinstance(rel.argument, str)]
                    problematic = ["Quote", "Project"]
                    for prob_rel in problematic:
                        if prob_rel in client_rels:
                            self.issues.append(f"❌ {model_name}: Still has {prob_rel} relationship - should be commented out")
                            logger.error(f"❌ {model_name}: Still has {prob_rel} relationship - should be commented out")
                        else:
                            logger.info(f"✅ {model_name}: {prob_rel} relationship properly removed/commented")
                            
            except Exception as e:
                logger.error(f"❌ Error checking {model_name}: {e}")
                self.issues.append(f"❌ Error checking {model_name}: {e}")
    
    def run_all_tests(self, base_class):
        """Run all tests and return a summary."""
        logger.info("🚀 Starting SQLAlchemy model tests...")
        
        # Setup
        if not self.setup_database():
            return False
        
        if not self.discover_models(base_class):
            return False
        
        # Run tests
        self.test_model_imports()
        self.test_model_relationships()
        self.check_common_issues()
        
        if self.test_table_creation():
            self.test_basic_crud()
            self.test_foreign_keys()
        
        # Summary
        self.print_summary()
        
        return len(self.issues) == 0
    
    def print_summary(self):
        """Print test summary."""
        logger.info("\n" + "="*60)
        logger.info("📊 TEST SUMMARY")
        logger.info("="*60)
        
        if not self.issues:
            logger.info("🎉 All tests passed! No issues found.")
        else:
            logger.info(f"❌ Found {len(self.issues)} issues:")
            for issue in self.issues:
                logger.info(f"   {issue}")
        
        logger.info("="*60)


def main():
    """Main function to run the model tests."""
    
    # Import your project's models - updated to match your actual structure
    try:
        from app.database import Base  # Base class for models
        from app.models.user import User
        from app.models.client import Client
        from app.models.invoice import Invoice, InvoiceItem  # Both in same file
        from app.models.product import Product
        from app.models.payment import Payment
        # Note: Quote and Project models don't exist yet (commented out in relationships)
        
        logger.info("✅ All model imports successful")
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("Please modify the imports in the main() function to match your project structure")
        logger.error("Available model files:")
        import os
        model_dir = "app/models"
        if os.path.exists(model_dir):
            for file in os.listdir(model_dir):
                if file.endswith('.py') and not file.startswith('__'):
                    logger.error(f"  - {file}")
        return False
    
    # Create tester instance
    # Use your actual database URL for more realistic testing
    # tester = ModelTester("postgresql://user:password@localhost:5432/dbname")
    tester = ModelTester("sqlite:///:memory:")  # Safe in-memory testing
    
    # Run tests
    success = tester.run_all_tests(Base)
    
    if success:
        logger.info("🎉 All model tests completed successfully!")
    else:
        logger.error("❌ Model tests completed with issues. Check the output above.")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
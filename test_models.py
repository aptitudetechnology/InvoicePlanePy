"""
Test script to verify database models work correctly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from app.models.base import BaseModel

def test_model_creation():
    """Test that all models can be created without errors"""
    try:
        # Import all models to register them
        from app.models import user, client, invoice, product, payment
        
        # Create all tables
        BaseModel.metadata.create_all(bind=engine)
        print("✅ All database tables created successfully!")
        
        # Print table information
        print("\n📋 Created tables:")
        for table_name in BaseModel.metadata.tables.keys():
            print(f"   - {table_name}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing database model creation...")
    success = test_model_creation()
    
    if success:
        print("\n🎉 All models are working correctly!")
        print("Ready to run: make dev-setup")
    else:
        print("\n💥 There are still issues to fix.")
        sys.exit(1)

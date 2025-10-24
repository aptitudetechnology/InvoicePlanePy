#!/usr/bin/env python3
"""
Quick test to verify setup manager imports work correctly
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        print("🔍 Testing imports...")
        
        # Test app.config import
        from app.config import settings
        print("✅ app.config imported successfully")
        
        # Test app.core.security import
        from app.core.security import get_password_hash
        print("✅ app.core.security imported successfully")
        
        # Test setup manager import
        from setup.setup_manager import SetupManager
        print("✅ setup.setup_manager imported successfully")
        
        # Test basic functionality
        setup_manager = SetupManager()
        print("✅ SetupManager instance created successfully")
        
        print("\n🎉 All imports working correctly!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)

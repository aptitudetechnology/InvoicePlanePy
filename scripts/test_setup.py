#!/usr/bin/env python3
"""
Test the setup process locally
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from setup.setup_manager import SetupManager

def main():
    print("🧪 Testing Setup Manager...")
    
    setup_manager = SetupManager()
    
    # Test individual steps
    print("\n1. Testing prerequisites...")
    step = setup_manager.check_prerequisites()
    if not step.completed:
        print(f"❌ Prerequisites failed: {step.error}")
        return False
    
    print("\n2. Testing database connection...")
    step = setup_manager.check_database_connection()
    if not step.completed:
        print(f"❌ Database connection failed: {step.error}")
        return False
    
    print("\n✅ Basic setup tests passed!")
    print("\nTo run full setup:")
    print("  make setup")
    print("  # or")
    print("  python setup/setup_manager.py")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

#!/usr/bin/env python3

import sys
import os
sys.path.append('/app')

from sqlalchemy.orm import Session
from app.database import get_db
from app.models.quotes import Quote, QuoteStatus
from fastapi import HTTPException

def debug_update_quote(quote_id: int, new_status: str, db: Session) -> bool:
    """
    Debug function to test quote status updates
    Returns True if successful, False if failed
    """
    try:
        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        if not quote:
            print(f"Quote {quote_id} not found")
            return False
            
        print(f"Before update: {quote.__dict__}")
        print(f"Attempting to set status to: {new_status}")
        
        # Try different variations
        variations = [
            (new_status, f"Direct string '{new_status}'"),
            (new_status.upper(), f"Uppercase '{new_status.upper()}'"),
            (getattr(QuoteStatus, new_status.upper(), None), f"Enum attribute '{new_status.upper()}'")
        ]
        
        for value, description in variations:
            if value is None:
                continue
                
            try:
                quote.status = value
                db.commit()
                print(f"✅ {description} succeeded")
                print(f"After update: {quote.__dict__}")
                return True
            except Exception as e:
                print(f"✗ {description} failed: {e}")
                db.rollback()
        
        print("❌ All status variations failed")
        return False
        
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        return False

def main():
    """Main function to test quote status updates"""
    # Get database session
    db = next(get_db())
    
    # Test with quote ID 1 (adjust as needed)
    quote_id = 1
    
    # Test different status values
    test_statuses = [
        'approved',
        'draft', 
        'DRAFT',
        'sent',
        'SENT',
        'accepted',
        'ACCEPTED',
        'converted',
        'CONVERTED',
        'rejected',
        'REJECTED'
    ]
    
    print("=== Quote Status Update Debug ===")
    print(f"Testing quote ID: {quote_id}")
    print(f"Available QuoteStatus enum values: {[status.value for status in QuoteStatus]}")
    print()
    
    # Test each status until one works
    for status in test_statuses:
        print(f"\nTesting status: '{status}'")
        print("-" * 40)
        
        success = debug_update_quote(quote_id, status, db)
        
        if success:
            print(f"✅ Status '{status}' SUCCESS - First working status found!")
            break
        else:
            print(f"❌ Status '{status}' FAILED - Trying next status...")
    else:
        print("\n❌ All test statuses failed!")
    
    # Close database session
    db.close()

if __name__ == "__main__":
    main()
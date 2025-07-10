from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, date
import sys
# --- CONFIGURE THIS ---
import os
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in the environment")

# Import your Quote model and QuoteStatus enum
try:
    from app.models.quotes import Quote, QuoteStatus
except ImportError:
    print("Could not import Quote or QuoteStatus. Check your import paths.")
    sys.exit(1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_quote_status_values():
    """Test what values are available in QuoteStatus enum"""
    print("Available QuoteStatus values:")
    for status in QuoteStatus:
        print(f"  {status.name} = '{status.value}'")
    print()

def debug_update_quote(quote_id, new_data):
    db = SessionLocal()
    try:
        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        assert quote is not None, "Quote not found"
        print("Before update:", quote.__dict__)
        
        # Assert required fields
        assert "client_id" in new_data, "client_id is required"
        assert "quote_number" in new_data, "quote_number is required"
        assert "status" in new_data, "status is required"
        assert "issue_date" in new_data, "issue_date is required"
        
        # Update fields
        quote.client_id = new_data["client_id"]
        quote.quote_number = new_data["quote_number"]
        
        # Try different approaches to set status
        status_value = new_data["status"]
        print(f"Attempting to set status to: {status_value}")
        
        # Try multiple approaches
        try:
            # Approach 1: Direct string value
            quote.status = QuoteStatus(status_value)
            print(f"✓ Direct string '{status_value}' worked")
        except ValueError as e1:
            print(f"✗ Direct string '{status_value}' failed: {e1}")
            
            # Approach 2: Uppercase string
            try:
                quote.status = QuoteStatus(status_value.upper())
                print(f"✓ Uppercase '{status_value.upper()}' worked")
            except ValueError as e2:
                print(f"✗ Uppercase '{status_value.upper()}' failed: {e2}")
                
                # Approach 3: Try to get enum by name
                try:
                    quote.status = getattr(QuoteStatus, status_value.upper())
                    print(f"✓ Enum attribute '{status_value.upper()}' worked")
                except AttributeError as e3:
                    print(f"✗ Enum attribute '{status_value.upper()}' failed: {e3}")
                    
                    # Approach 4: Try common variations
                    variations = [
                        status_value.lower(),
                        status_value.capitalize(),
                        status_value.title(),
                        f"{status_value.upper()}",
                        f"{status_value.lower()}"
                    ]
                    
                    success = False
                    for variation in variations:
                        try:
                            quote.status = QuoteStatus(variation)
                            print(f"✓ Variation '{variation}' worked")
                            success = True
                            break
                        except ValueError:
                            continue
                    
                    if not success:
                        print("❌ All status variations failed")
                        raise ValueError(f"Could not set status to any variation of '{status_value}'")
        
        quote.notes = new_data.get("notes", quote.notes)
        
        # Parse and update dates
        try:
            quote.issue_date = datetime.strptime(new_data["issue_date"], "%Y-%m-%d").date()
        except Exception as e:
            print("Invalid issue_date:", new_data["issue_date"])
            raise
        
        valid_until = new_data.get("valid_until")
        if valid_until:
            try:
                quote.valid_until = datetime.strptime(valid_until, "%Y-%m-%d").date()
            except Exception as e:
                print("Invalid valid_until:", valid_until)
                raise
        else:
            quote.valid_until = None
        
        quote.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(quote)
        print("After update:", quote.__dict__)
        print("Quote updated successfully.")
        
    except AssertionError as ae:
        print("AssertionError:", ae)
    except Exception as e:
        db.rollback()
        print("Error updating quote:", e)
    finally:
        db.close()

def test_multiple_status_values(quote_id):
    """Test multiple status values to see which ones work"""
    test_statuses = [
        "approved",
        "APPROVED", 
        "draft",
        "DRAFT",
        "sent",
        "SENT",
        "accepted",
        "ACCEPTED",
        "converted",
        "CONVERTED",
        "pending",
        "PENDING",
        "rejected",
        "REJECTED"
    ]
    
    print("Testing multiple status values:")
    print("-" * 50)
    
    for status in test_statuses:
        print(f"\nTesting status: '{status}'")
        try:
            debug_update_quote(
                quote_id=quote_id,
                new_data={
                    "client_id": 2,
                    "quote_number": "QUO-9999",
                    "status": status,
                    "issue_date": "2025-07-10",
                    "valid_until": "2025-07-31",
                    "notes": f"Updated via debug script with status {status}"
                }
            )
            print(f"✅ Status '{status}' SUCCESS")
            break  # Stop after first success
        except Exception as e:
            print(f"❌ Status '{status}' FAILED: {e}")
            continue

if __name__ == "__main__":
    # First, show what enum values are available
    test_quote_status_values()
    
    # Then test multiple values
    test_multiple_status_values(quote_id=1)
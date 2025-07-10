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
        try:
            quote.status = QuoteStatus(new_data["status"])
        except Exception as e:
            print("Invalid status value:", new_data["status"])
            raise

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

if __name__ == "__main__":
    # Example usage: update quote with id=1
    debug_update_quote(
        quote_id=1,
        new_data={
            "client_id": 2,
            "quote_number": "QUO-9999",
            "status": "draft",  # or "approved", etc.
            "issue_date": "2025-07-10",
            "valid_until": "2025-07-31",
            "notes": "Updated via debug script"
        }
    )
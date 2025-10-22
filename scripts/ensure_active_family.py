#!/usr/bin/env python3
"""
Ensure at least one active product family exists for modal testing.
"""
from app.database import SessionLocal
from app.models.product import ProductFamily

def main():
    db = SessionLocal()
    try:
        families = db.query(ProductFamily).all()
        print(f"Found {len(families)} families:")
        for fam in families:
            print(f"  - {fam.id}: {fam.name} (active={fam.is_active})")
        if not families:
            print("No families found. Creating a test family...")
            fam = ProductFamily(name="Test Family", is_active=True)
            db.add(fam)
            db.commit()
            print("Test family created!")
        elif not any(f.is_active for f in families):
            print("No active families. Activating the first one...")
            families[0].is_active = True
            db.commit()
            print(f"Activated family: {families[0].name}")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

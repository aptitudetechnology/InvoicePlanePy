#!/usr/bin/env python3
"""
Check and create sample product families if none exist
"""
from app.database import SessionLocal
from app.models.product import ProductFamily

def main():
    db = SessionLocal()
    try:
        # Check existing families
        families = db.query(ProductFamily).all()
        print(f"Found {len(families)} families in database:")

        for family in families:
            print(f"  - ID: {family.id}, Name: '{family.name}', Active: {family.is_active}")

        # If no families exist, create some sample ones
        if len(families) == 0:
            print("\nNo families found. Creating sample families...")

            sample_families = [
                {"name": "Electronics", "is_active": True},
                {"name": "Office Supplies", "is_active": True},
                {"name": "Furniture", "is_active": True},
                {"name": "Software", "is_active": True},
                {"name": "Services", "is_active": True}
            ]

            for family_data in sample_families:
                family = ProductFamily(**family_data)
                db.add(family)
                print(f"Created family: {family_data['name']}")

            db.commit()
            print("Sample families created successfully!")

            # Also create a sample product if none exist
            from app.models.product import Product
            products = db.query(Product).all()
            if len(products) == 0:
                print("\nNo products found. Creating a sample product...")
                sample_product = Product(
                    name="Sample Laptop",
                    sku="SL-001",
                    price=999.99,
                    family_id=1,  # Electronics
                    is_active=True
                )
                db.add(sample_product)
                db.commit()
                print("Sample product created!")

        else:
            print("\nFamilies already exist - no action needed.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
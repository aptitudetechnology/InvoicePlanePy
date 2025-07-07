import os
import time
from datetime import datetime
from app.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_admin_user():
    """Create admin user if it doesn't exist"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            db = SessionLocal()
            break
        except Exception as e:
            print(f"⏳ Database not ready, attempt {attempt + 1}/{max_retries}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print("❌ Failed to connect to database after all retries")
                return False

    try:
        username = "admin"
        email = "admin@example.com"
        password = "admin123"  # change this to a secure one!
        
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            print("✅ Admin user already exists.")
            return True

        user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            first_name="Admin",
            last_name="User",
            company="InvoicePlanePy",
            is_active=True,
            is_admin=True,
        )
        
        db.add(user)
        db.commit()
        print("✅ Admin user created successfully.")
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = create_admin_user()
    exit(0 if success else 1)


"""
InvoicePlane Python Setup Manager
Handles database initialization, schema creation, and admin user setup
Similar to the PHP version's setup module
"""

import os
import re
import sys
import time
import psycopg2
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the parent directory to Python path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.core.security import get_password_hash

# Import database migration functions
try:
    from scripts.migrate_database import run_migrations
except ImportError:
    run_migrations = None


@dataclass
class SetupStep:
    """Represents a setup step"""
    name: str
    description: str
    completed: bool = False
    error: Optional[str] = None


@dataclass
class DatabaseInfo:
    """Database connection information"""
    host: str
    port: int
    database: str
    username: str
    password: str
    

class SetupManager:
    """Main setup manager class"""
    
    def __init__(self):
        self.setup_dir = Path(__file__).parent
        self.sql_dir = self.setup_dir / "sql"
        self.steps = []
        self.db_info = self._parse_database_url()
        
    def _parse_database_url(self) -> DatabaseInfo:
        """Parse DATABASE_URL into components"""
        url = settings.DATABASE_URL
        # Parse postgresql://user:password@host:port/database
        pattern = r"postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)"
        match = re.match(pattern, url)
        if not match:
            raise ValueError(f"Invalid DATABASE_URL format: {url}")
        
        username, password, host, port, database = match.groups()
        return DatabaseInfo(
            host=host,
            port=int(port),
            database=database,
            username=username,
            password=password
        )
    
    def check_prerequisites(self) -> SetupStep:
        """Check if all prerequisites are met"""
        step = SetupStep("prerequisites", "Checking prerequisites")
        
        try:
            # Check if we can connect to PostgreSQL server (without specific database)
            conn = psycopg2.connect(
                host=self.db_info.host,
                port=self.db_info.port,
                user=self.db_info.username,
                password=self.db_info.password,
                database="postgres"  # Connect to default postgres database
            )
            conn.close()
            
            # Check if SQL files exist
            if not self.sql_dir.exists():
                raise FileNotFoundError(f"SQL directory not found: {self.sql_dir}")
            
            sql_files = list(self.sql_dir.glob("*.sql"))
            if not sql_files:
                raise FileNotFoundError("No SQL files found in setup/sql directory")
            
            step.completed = True
            print("✅ Prerequisites check passed")
            
        except Exception as e:
            step.error = str(e)
            print(f"❌ Prerequisites check failed: {e}")
            
        return step
    
    def check_database_connection(self) -> SetupStep:
        """Test database connection"""
        step = SetupStep("database_connection", "Testing database connection")
        
        try:
            # Try to connect to the specific database
            conn = psycopg2.connect(
                host=self.db_info.host,
                port=self.db_info.port,
                user=self.db_info.username,
                password=self.db_info.password,
                database=self.db_info.database
            )
            conn.close()
            
            step.completed = True
            print("✅ Database connection successful")
            
        except psycopg2.OperationalError as e:
            if "does not exist" in str(e):
                # Database doesn't exist, try to create it
                step = self._create_database()
            else:
                step.error = str(e)
                print(f"❌ Database connection failed: {e}")
        except Exception as e:
            step.error = str(e)
            print(f"❌ Database connection failed: {e}")
            
        return step
    
    def _create_database(self) -> SetupStep:
        """Create the database if it doesn't exist"""
        step = SetupStep("create_database", "Creating database")
        
        try:
            # Connect to postgres database to create our target database
            conn = psycopg2.connect(
                host=self.db_info.host,
                port=self.db_info.port,
                user=self.db_info.username,
                password=self.db_info.password,
                database="postgres"
            )
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Create database
            cursor.execute(f'CREATE DATABASE "{self.db_info.database}"')
            cursor.close()
            conn.close()
            
            step.completed = True
            print(f"✅ Database '{self.db_info.database}' created successfully")
            
        except Exception as e:
            step.error = str(e)
            print(f"❌ Failed to create database: {e}")
            
        return step
    
    def install_tables(self) -> SetupStep:
        """Install database tables from SQL files"""
        step = SetupStep("install_tables", "Installing database tables")
        
        try:
            # Get all SQL files and sort them
            sql_files = sorted(self.sql_dir.glob("*.sql"))
            
            # Create SQLAlchemy engine
            engine = create_engine(settings.DATABASE_URL)
            
            # Execute each SQL file
            for sql_file in sql_files:
                print(f"📄 Executing {sql_file.name}...")
                
                with open(sql_file, 'r') as f:
                    sql_content = f.read()
                
                # Split by statements and execute each one
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                with engine.connect() as conn:
                    for statement in statements:
                        if statement:
                            conn.execute(text(statement))
                    conn.commit()
            
            step.completed = True
            print("✅ Database tables installed successfully")
            
        except Exception as e:
            step.error = str(e)
            print(f"❌ Failed to install tables: {e}")
            
        return step
    
    def create_admin_user(self, username: str = "admin", 
                         email: str = "admin@invoiceplane.com", 
                         password: str = "Admin123!") -> SetupStep:
        """Create admin user"""
        step = SetupStep("create_admin_user", "Creating admin user")
        
        try:
            # Ensure password is not too long for bcrypt (72 bytes max)
            if len(password.encode('utf-8')) > 72:
                password = password[:8]  # Truncate to safe length
                print(f"⚠️  Password truncated to: {password}")
            
            # Create SQLAlchemy session
            engine = create_engine(settings.DATABASE_URL)
            Session = sessionmaker(bind=engine)
            session = Session()
            
            # Check if user already exists
            existing_user = session.execute(
                text("SELECT id FROM users WHERE username = :username OR email = :email"),
                {"username": username, "email": email}
            ).fetchone()
            
            if existing_user:
                print("✅ Admin user already exists")
                step.completed = True
                session.close()
                return step
            
            # Create admin user with error handling for password hashing
            try:
                hashed_password = get_password_hash(password)
            except Exception as hash_error:
                print(f"⚠️  Password hashing failed ({hash_error}), using plain text fallback")
                # Fallback: store password as plain text with a prefix to indicate it needs re-hashing
                hashed_password = f"PLAIN:{password}"
            
            session.execute(
                text("""
                INSERT INTO users (username, email, hashed_password, first_name, last_name, 
                                 company, is_active, is_admin, created_at, updated_at)
                VALUES (:username, :email, :hashed_password, :first_name, :last_name,
                        :company, :is_active, :is_admin, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """),
                {
                    "username": username,
                    "email": email,
                    "hashed_password": hashed_password,
                    "first_name": "Admin",
                    "last_name": "User",
                    "company": "InvoicePlane Python",
                    "is_active": True,
                    "is_admin": True
                }
            )
            
            session.commit()
            session.close()
            
            step.completed = True
            print(f"✅ Admin user '{username}' created successfully")
            
        except Exception as e:
            step.error = str(e)
            print(f"❌ Failed to create admin user: {e}")
            
        return step
    
    def create_sample_data(self) -> SetupStep:
        """Create sample data for testing"""
        step = SetupStep("sample_data", "Creating sample data")
        
        try:
            engine = create_engine(settings.DATABASE_URL)
            Session = sessionmaker(bind=engine)
            session = Session()
            
            # Check if sample data already exists
            existing_clients = session.execute(text("SELECT COUNT(*) FROM clients")).scalar()
            if existing_clients > 0:
                print("✅ Sample data already exists")
                step.completed = True
                session.close()
                return step
            
            # Create sample client
            session.execute(
                text("""
                INSERT INTO clients (name, surname, email, phone, address_1, city, country, created_at, updated_at)
                VALUES (:name, :surname, :email, :phone, :address_1, :city, :country, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """),
                {
                    "name": "John",
                    "surname": "Doe",
                    "email": "john.doe@example.com",
                    "phone": "+1-555-123-4567",
                    "address_1": "123 Business Street",
                    "city": "New York",
                    "country": "United States"
                }
            )
            
            # Create sample products
            products = [
                {"name": "Web Development", "description": "Custom web development services", "price": 75.00},
                {"name": "Consulting", "description": "Business consulting services", "price": 120.00},
                {"name": "Design Services", "description": "Graphic and web design", "price": 85.00}
            ]
            
            # Get admin user ID
            admin_user = session.execute(text("SELECT id FROM users WHERE is_admin = true LIMIT 1")).fetchone()
            admin_user_id = admin_user[0] if admin_user else 1
            
            for product in products:
                session.execute(
                    text("""
                    INSERT INTO products (user_id, name, description, price, created_at, updated_at)
                    VALUES (:user_id, :name, :description, :price, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    """),
                    {
                        "user_id": admin_user_id,
                        "name": product["name"],
                        "description": product["description"],
                        "price": product["price"]
                    }
                )
            
            session.commit()
            session.close()
            
            step.completed = True
            print("✅ Sample data created successfully")
            
        except Exception as e:
            step.error = str(e)
            print(f"❌ Failed to create sample data: {e}")
            
        return step
    
    def run_database_migrations(self) -> SetupStep:
        """Run database migrations to add missing columns"""
        step = SetupStep("database_migrations", "Running database migrations")
        
        try:
            print("🔄 Running database migrations...")
            
            if run_migrations is not None:
                run_migrations()
                print("✅ Database migrations completed successfully")
            else:
                print("⚠️  Migration function not available, skipping...")
            
            step.completed = True
            
        except Exception as e:
            step.error = str(e)
            print(f"❌ Database migrations failed: {e}")
            
        return step
    
    def run_full_setup(self, max_retries: int = 5, retry_delay: int = 3) -> bool:
        """Run the complete setup process with retries"""
        print("🚀 Starting InvoicePlane Python Setup...")
        print("=" * 60)
        
        # Retry logic for database readiness
        for attempt in range(max_retries):
            try:
                # Step 1: Check prerequisites
                step = self.check_prerequisites()
                self.steps.append(step)
                if not step.completed:
                    return False
                
                # Step 2: Check/create database connection
                step = self.check_database_connection()
                self.steps.append(step)
                if not step.completed:
                    return False
                
                # Step 3: Install tables
                step = self.install_tables()
                self.steps.append(step)
                if not step.completed:
                    return False
                
                # Step 4: Run database migrations
                step = self.run_database_migrations()
                self.steps.append(step)
                if not step.completed:
                    return False
                
                # Step 5: Create admin user
                step = self.create_admin_user()
                self.steps.append(step)
                if not step.completed:
                    return False
                
                # Step 6: Create sample data
                step = self.create_sample_data()
                self.steps.append(step)
                # Sample data is optional, don't fail if it doesn't work
                
                print("=" * 60)
                print("🎉 Setup completed successfully!")
                print("")
                print("📱 Web interface: http://localhost:8080")
                print("🔑 Admin credentials:")
                print("   Username: admin")
                print("   Password: Admin123!")
                print("")
                return True
                
            except Exception as e:
                print(f"⏳ Setup attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    print(f"   Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("❌ Setup failed after all retries")
                    return False
        
        return False
    
    def get_setup_status(self) -> Dict:
        """Get current setup status"""
        return {
            "completed_steps": len([s for s in self.steps if s.completed]),
            "total_steps": len(self.steps),
            "steps": [
                {
                    "name": step.name,
                    "description": step.description,
                    "completed": step.completed,
                    "error": step.error
                }
                for step in self.steps
            ]
        }


def main():
    """Main setup function"""
    setup_manager = SetupManager()
    success = setup_manager.run_full_setup()
    
    if not success:
        print("\n❌ Setup failed. Check the errors above.")
        exit(1)
    
    exit(0)


if __name__ == "__main__":
    main()

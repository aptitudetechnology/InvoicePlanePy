#!/usr/bin/env python3
"""
check_db_schema.py

Compares the live PostgreSQL database schema to the SQLAlchemy ORM models.
Prints a summary of mismatches and suggests ALTER TABLE statements if needed.

Usage:
    python scripts/check_db_schema.py
"""
import os
import sys
from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# --- CONFIGURATION ---
# Use the same DATABASE_URL as the app
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("[ERROR] DATABASE_URL environment variable not set.")
    sys.exit(1)

# Import all models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))
from app import models  # noqa: F401
from app.models import *  # noqa: F403, F401

from app.database import Base  # Use the same Base as all models

# --- SCHEMA CHECK LOGIC ---
def get_model_tables():
    """Return a dict of {table_name: model_class}"""
    tables = {}
    for obj in models.__dict__.values():
        if hasattr(obj, "__table__"):
            tables[obj.__table__.name] = obj
    return tables

def compare_columns(model_cols, db_cols):
    mismatches = []
    model_col_names = set(model_cols.keys())
    db_col_names = set(db_cols.keys())
    missing_in_db = model_col_names - db_col_names
    extra_in_db = db_col_names - model_col_names
    for col in missing_in_db:
        mismatches.append(f"[MISSING IN DB] Column '{col}' defined in model but missing in DB.")
    for col in extra_in_db:
        mismatches.append(f"[EXTRA IN DB] Column '{col}' exists in DB but not in model.")
    for col in model_col_names & db_col_names:
        mcol = model_cols[col]
        dcol = db_cols[col]
        # Compare type
        if str(mcol['type']).lower() != str(dcol['type']).lower():
            mismatches.append(f"[TYPE MISMATCH] Column '{col}': model={mcol['type']} db={dcol['type']}")
        # Compare nullability
        if mcol['nullable'] != dcol['nullable']:
            mismatches.append(f"[NULLABLE MISMATCH] Column '{col}': model={mcol['nullable']} db={dcol['nullable']}")
    return mismatches

def main():
    print("\n🔍 Checking database schema against ORM models...\n")
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    model_tables = get_model_tables()
    found_mismatches = False
    for table_name, model in model_tables.items():
        print(f"--- Table: {table_name} ---")
        if table_name not in inspector.get_table_names():
            print(f"[MISSING IN DB] Table '{table_name}' defined in model but missing in DB.")
            found_mismatches = True
            continue
        # Get model columns
        model_cols = {}
        for col in model.__table__.columns:
            model_cols[col.name] = {
                'type': col.type,
                'nullable': col.nullable
            }
        # Get db columns
        db_cols = {}
        for col in inspector.get_columns(table_name):
            db_cols[col['name']] = {
                'type': col['type'],
                'nullable': col['nullable']
            }
        mismatches = compare_columns(model_cols, db_cols)
        if mismatches:
            found_mismatches = True
            for m in mismatches:
                print(m)
        else:
            print("[OK] Table matches model.")
        print()
    if found_mismatches:
        print("❌ Schema mismatches found. Please review the above output.\n")
        # Ask if user wants to make a backup
        backup = input("Would you like to make a backup of the live database before purging? [y/N]: ").strip().lower()
        if backup == 'y':
            # Attempt to run pg_dump
            import subprocess
            backup_file = f"db_backup_$(date +%Y%m%d_%H%M%S).sql"
            print(f"Backing up database to {backup_file}...")
            try:
                # Parse DB URL for pg_dump
                from sqlalchemy.engine.url import make_url
                url = make_url(DATABASE_URL)
                pg_dump_cmd = [
                    "pg_dump",
                    f"-h", url.host or 'localhost',
                    f"-U", url.username,
                    f"-p", str(url.port or 5432),
                    f"-d", url.database,
                    f"-f", backup_file
                ]
                env = os.environ.copy()
                if url.password:
                    env["PGPASSWORD"] = url.password
                subprocess.run(pg_dump_cmd, check=True, env=env)
                print(f"[OK] Backup complete: {backup_file}")
            except Exception as e:
                print(f"[ERROR] Backup failed: {e}")
        # Ask if user wants to purge
        purge = input("Do you want to PURGE (drop and recreate) the live database to match the models? [y/N]: ").strip().lower()
        if purge == 'y':
            print("Purging and recreating the database...")
            try:
                # Drop all tables and recreate
                from sqlalchemy_utils import database_exists, create_database, drop_database
                if database_exists(engine.url):
                    drop_database(engine.url)
                create_database(engine.url)
                Base.metadata.create_all(engine)
                print("[OK] Database purged and recreated.")
            except ImportError:
                print("[ERROR] sqlalchemy_utils is required for purge. Install with 'pip install sqlalchemy-utils'.")
            except Exception as e:
                print(f"[ERROR] Purge failed: {e}")
        else:
            print("Purge cancelled. No changes made.")
        sys.exit(2)
    else:
        print("✅ All tables match ORM models.")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except SQLAlchemyError as e:
        print(f"[ERROR] SQLAlchemy error: {e}")
        sys.exit(3)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(4)

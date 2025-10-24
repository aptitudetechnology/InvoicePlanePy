# Plan: Integrate Database Schema Check at Startup

## Goal
Automatically compare the live PostgreSQL database schema to the SQLAlchemy ORM models at startup, and report any mismatches before the FastAPI server starts.

## Steps

1. **Implement Schema Check Script**
   - Create a script (e.g., `scripts/check_db_schema.py`) that:
     - Connects to the database using SQLAlchemy.
     - Reflects the live schema using SQLAlchemy's Inspector.
     - Iterates over all ORM models and compares expected vs. actual columns, types, and nullability.
     - Prints a summary of mismatches and (optionally) suggests `ALTER TABLE` statements.

2. **Update Startup Script**
   - In `startup.sh`, after the database is ready and before starting the FastAPI server:
     - Run the schema check script:
       ```bash
       echo "🔍 Checking database schema against ORM models..."
       python scripts/check_db_schema.py
       ```
     - If mismatches are found, print them clearly. Optionally, exit with an error code to block startup if critical mismatches are detected.

3. **Requirements**
   - Ensure `SQLAlchemy >= 1.4` and `psycopg2` are installed.
   - The script should use the same `DATABASE_URL` as the app.

4. **(Optional) CI Integration**
   - Add the schema check script to CI pipelines to catch schema drift early.

5. **Documentation**
   - Document this process in the README and developer onboarding docs.
   - Mention how to run the check manually and interpret results.

## Example Startup Sequence
1. Wait for database to be ready
2. Run setup/initialization scripts
3. **Run schema check script**
4. Start FastAPI server

---

**This plan ensures that schema mismatches are detected early, reducing runtime errors and improving reliability.**

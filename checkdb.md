"""
GitHub Copilot instructions:

Goal:
Compare the live PostgreSQL database schema to the SQLAlchemy ORM models and identify any mismatches (e.g., missing columns, wrong types, missing tables).

Steps:
1. Connect to the PostgreSQL database using SQLAlchemy's engine.
2. Reflect the live database schema using SQLAlchemy's `Inspector`.
3. Iterate over each SQLAlchemy model defined in the ORM.
4. For each model:
    - Get the table name and expected columns (name, type, nullable).
    - Get the actual columns from the live database using Inspector.
    - Compare actual vs expected:
        - Missing columns
        - Extra columns
        - Type mismatches
        - Nullability mismatches
5. Print a summary of all mismatches per table.
6. (Optional) Suggest ALTER TABLE statements to fix schema.

Requirements:
- SQLAlchemy >= 1.4
- PostgreSQL connection URL in environment or config (e.g., `DATABASE_URL`)
"""

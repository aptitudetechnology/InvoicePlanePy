import os
import psycopg2
from urllib.parse import urlparse

# Get DATABASE_URL from environment or .env.example
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # Fallback: try to read from .env.example
    with open(".env.example") as f:
        for line in f:
            if line.startswith("DATABASE_URL="):
                DATABASE_URL = line.strip().split("=", 1)[1]
                break

if not DATABASE_URL:
    print("DATABASE_URL not found in environment or .env.example!")
    exit(1)

print(f"Using DATABASE_URL: {DATABASE_URL}")

# Parse the URL for psycopg2
url = urlparse(DATABASE_URL)
conn = psycopg2.connect(
    dbname=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cur = conn.cursor()

# Check if tax_rate table exists
cur.execute("SELECT tablename FROM pg_tables WHERE tablename = 'tax_rate';")
exists = cur.fetchone()
if exists:
    print("tax_rate table exists.")
    cur.execute("SELECT * FROM tax_rate LIMIT 5;")
    rows = cur.fetchall()
    print("Sample data:")
    for row in rows:
        print(row)
else:
    print("tax_rate table does NOT exist.")

cur.close()
conn.close()

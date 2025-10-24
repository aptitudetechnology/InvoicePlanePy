#!/bin/bash
set -e

echo "🚀 Starting InvoicePlane Python application..."

# Set default port if not provided
PORT=${PORT:-8080}

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
python -c "
import time
import psycopg2
from app.config import settings

for i in range(30):
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        conn.close()
        print('✅ Database is ready!')
        break
    except psycopg2.OperationalError:
        print(f'Database not ready yet, waiting... ({i+1}/30)')
        time.sleep(2)
else:
    print('❌ Database failed to become ready')
    exit(1)
"

# Run the comprehensive setup process
echo "🔧 Running database setup..."
export PYTHONPATH=/app
cd /app
python setup/setup_manager.py

echo "✅ Startup complete!"

# Start the FastAPI application
echo "🌐 Starting web server on port ${PORT}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}

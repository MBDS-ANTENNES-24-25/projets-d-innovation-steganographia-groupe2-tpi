#!/bin/sh
set -e

# Ensure alembic folder exists
if [ ! -d "./alembic" ]; then
    echo "Alembic folder not found, initializing..."
    alembic init alembic
fi

# Generate initial migration if none exist
if [ -z "$(ls -A alembic/versions 2>/dev/null)" ]; then
    echo "No migrations found, generating initial migration..."
    alembic revision --autogenerate -m "initial migration"
fi

# Apply migrations
echo "Applying migrations..."
alembic upgrade head

# Start the application
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

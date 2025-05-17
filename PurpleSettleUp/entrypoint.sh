#!/bin/bash

# Wait for DB
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done

# Run migrations
python manage.py migrate

# Start Gunicorn with Uvicorn worker
exec gunicorn myproject.asgi:application \
  --bind 0.0.0.0:8001 \
  -k uvicorn.workers.UvicornWorker
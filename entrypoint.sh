#!/bin/bash

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.5
done
echo "PostgreSQL is ready."

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "👉 Applying migrations..."
python manage.py migrate --noinput

echo "🚀 Starting Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8001 --workers 3 --timeout 30 --graceful-timeout 10
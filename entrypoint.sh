#!/bin/sh

echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Database is up"

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "Creating migrations"
python manage.py makemigrations

echo "👉 Applying migrations..."
python manage.py migrate --noinput

python manage.py collectstatic --noinput

gunicorn core.wsgi:application --bind 0.0.0.0:8000

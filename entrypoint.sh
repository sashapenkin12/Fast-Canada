#!/bin/bash
echo "👉 Выполняем миграции..."
python manage.py migrate --noinput

echo "🚀 Запускаем Gunicorn..."
gunicorn --bind 0.0.0.0:8001 --workers 3 core.wsgi:application
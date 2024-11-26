#!/usr/bin/env sh

python manage.py makemigrations 
python manage.py migrate
python manage.py collectstatic --noinput

echo "Запуск Django с помощью Gunicorn..."

gunicorn bot_backend.wsgi:application --bind 0.0.0.0:8000 --reload

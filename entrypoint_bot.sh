#!/usr/bin/env sh

python manage.py makemigrations 
python manage.py migrate

echo "${0}: running telegram bot."

python manage.py startbot
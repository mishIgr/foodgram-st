#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py loaddata dump/db.json
gunicorn --bind 0.0.0.0:8000 foodgram.wsgi
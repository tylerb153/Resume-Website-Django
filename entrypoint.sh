#!/bin/bash
echo "Migrating database"
python manage.py migrate --noinput

echo "Collecting static"
python manage.py collectstatic --noinput

echo "Starting webserver"
exec gunicorn --bind 0.0.0.0:8000 minecraftcultsite.wsgi:application
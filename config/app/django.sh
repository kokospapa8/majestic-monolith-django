#!/usr/bin/env bash
# Migrate created migrations to database

# Start gunicorn server at port 8000 and keep an eye for app code changes
# If changes occur, kill worker and start a new one
curl 169.254.170.2$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI
echo "export AWS_CONTAINER_CREDENTIALS_RELATIVE_URI=$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI" >> /root/.profile

python manage.py migrate
python manage.py collectstatic --no-input
gunicorn majestic-monolith-django.asgi:application -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -w 3 --reload

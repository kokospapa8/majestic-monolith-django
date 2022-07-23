#!/usr/bin/env bash
python manage.py migrate
python manage.py collectstatic --no-input
gunicorn majestic-monolith-django.asgi:application -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -w 3 --reload

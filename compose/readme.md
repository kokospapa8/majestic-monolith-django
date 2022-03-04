asgi
gunicorn majestic-monolith-django.asgi:application -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -w 3

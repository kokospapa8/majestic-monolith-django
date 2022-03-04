"""
ASGI config for daas project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

ENV = os.environ.get("ENV", "local")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'majestic-monolith-django.settings.{ENV}')

application = get_asgi_application()

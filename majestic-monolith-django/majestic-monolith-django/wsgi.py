"""
WSGI config for daas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

ENV = os.environ.get("ENV", "dev")
if ENV in ["beta", "prod"]:
    settings = f"majestic-monolith-django.settings_{ENV}"
else:
    settings = "majestic-monolith-django.settings"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'majestic-monolith-django.settings')

application = get_wsgi_application()

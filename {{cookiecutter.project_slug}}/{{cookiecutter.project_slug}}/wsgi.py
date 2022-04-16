"""
WSGI config for {{cookiecutter.project_slug}} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

ENV = os.environ.get("ENV", "dev")
if ENV in ["beta", "prod"]:
    settings = f"{{cookiecutter.project_slug}}.settings_{ENV}"
else:
    settings = "{{cookiecutter.project_slug}}.settings"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{cookiecutter.project_slug}}.settings')

application = get_wsgi_application()

#!/usr/bin/env bash
python manage.py migrate
pytest --ds=settings.test

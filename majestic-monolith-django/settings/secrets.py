# -*- coding: utf-8 -*-
import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_env_variable("SECRET_KEY")
DB_USERNAME = get_env_variable("DB_USERNAME")
DB_PASSWORD = get_env_variable("DB_PASSWORD")
DB_HOST = get_env_variable("DB_HOST")
REDIS_HOST = get_env_variable("REDIS_HOST")
S3_BUCKET = get_env_variable("S3_BUCKET")
SLACK_TOKEN = get_env_variable("SLACK_TOKEN")
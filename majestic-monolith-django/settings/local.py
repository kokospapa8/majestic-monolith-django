# -*- coding: utf-8 -*-

from .app import *
from .base import *
from .packages.auth import *
from .packages.email import *
from .packages.push import *
from .packages.swagger import *
from .packages.rest import *
from .secrets import *
from .packages.logger import *
from .packages.slack import *

logger = logging.getLogger("django.debuglogger")

DEBUG = True


################################################################
# COMMON BLOCK FOR ENV FILE
################################################################
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        from django.core.exceptions import ImproperlyConfigured

        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)


ENV = get_env_variable("ENV")
ENV_ALIAS = ENV


# make sure to include this on each environment
SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY

BASE_DIR = Path(__file__).resolve().parent.parent


logger.debug(f"CURRENT ENVIRONMENT: {ENV}")
logger.debug(f"Base DIR: {BASE_DIR}")
################################################################
# END - COMMON BLOCK FOR ENV FILE
################################################################

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
#
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": f"sample",
#         "USER": DB_USERNAME,
#         "PASSWORD": DB_PASSWORD,
#         "HOST": "127.0.0.1",  # Or an IP Address that your DB is hosted on
#         "PORT": "3306",
#         "CONN_MAX_AGE": 60 * 5,
#         "OPTIONS": {
#             "init_command": "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1, read_rnd_buffer_size=256000",
#             "charset": "utf8mb4",
#         },
#         "TEST": {"CHARSET": "utf8mb4", "COLLATION": "utf8mb4_unicode_ci"},
#     }
# }

CACHES = {
    "default": {
        # "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": f"redis://{REDIS_HOST}:6379/1",
        # "OPTIONS": {
        #     "CLIENT_CLASS": "django_redis.client.DefaultClient",
        #     "IGNORE_EXCEPTION": True,  # needed for redis is only cache
        #     "PARSER_CLASS": "redis.connection.HiredisParser",
        # },

        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',

    }
}

# this only for development
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# if you don't already have this in settings
DEFAULT_FROM_EMAIL = "server@exammple.com"

# AWS
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

# LOCALStorages
STATIC_URL = "/static/"
STATIC_ROOT = "/Users/jinwookbaek/Project/majestic-monolith-django/static"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# s3 remote static
# STATIC_URL = "https://media-dev.example.co.kr/"
# DEFAULT_FILE_STORAGE = "core.storages.CustomS3Boto3Storages"
# STATICFILES_STORAGE = "core.storages.CustomS3Boto3Storages"
#
# AWS_STORAGE_BUCKET_NAME = S3_BUCKET
# AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "ap-northeast-2")
# CORS_ORIGIN_ALLOW_ALL = True
# AWS_QUERYSTRING_AUTH = False
# AWS_DEFAULT_ACL = "public-read"


INSTALLED_APPS.extend(["django_extensions"])
MIDDLEWARE.extend(["django.middleware.csrf.CsrfViewMiddleware"])

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
    'rest_framework.renderers.JSONRenderer',
    "rest_framework.renderers.BrowsableAPIRenderer",
)

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
    "core.authentication.MMDJWTAuthentication",
    "rest_framework.authentication.SessionAuthentication",
)

TESTING = ENV == "test"

THUMBNAIL_DEFAULT_STORAGE = (
    'easy_thumbnails.storage.ThumbnailFileSystemStorage')

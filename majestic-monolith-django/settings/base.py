# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path

from django.conf.locale.en import formats as es_format

BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = "user.CustomUser"

ADMINS = [("Jinwook Baek", "kokos.papa8@gmail.com")]
MANAGERS = ADMINS

INSTALLED_APPS = [
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "auth.apps.AuthConfig",
    "user.apps.UserConfig",
    "distribution.apps.DistributionConfig",
    "shipping.apps.ShippingConfig",
    "django_mysql",
    "corsheaders",
    "rest_framework",
    "rest_framework_api_key",
    "rest_framework_word_filter",
    "drf_yasg",
    "drf_spectacular",
    "allauth",
    "allauth.account",
    "phonenumber_field",
    "django_filters",
    "django_guid",
    "django_user_agents",
    "daterangefilter",
    "easy_thumbnails",
    "aws_xray_sdk.ext.django",
]

MIDDLEWARE = [
    "aws_xray_sdk.ext.django.middleware.XRayMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "core.middleware.HealthCheckMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "django_guid.middleware.guid_middleware",
    "core.middleware.MMDLoggingMiddleware",
]

ROOT_URLCONF = "majestic-monolith-django.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processor.static_url",
                "django.template.context_processors.i18n",
            ]
        },
    }
]

WSGI_APPLICATION = "majestic-monolith-django.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "core.password_validation.MaximumLengthValidator",
        "OPTIONS": {
            "max_length": 16,
        },
    },
    {"NAME": "core.password_validation.AlphaNumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en"


LANGUAGES = [
    ("en", "English"),
    ("ko", "Korean"),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "../locale"),
]

# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# for django admin default datetime format
es_format.DATETIME_FORMAT = "Y-m-d H:i:s"

# django-activity-stream
ACTSTREAM_SETTINGS = {
    "USE_JSONFIELD": True,
}

# Storages
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
AWS_STORAGE_BUCKET_NAME = ""
AWS_S3_REGION_NAME = "ap-northeast-2"
AWS_QUERYSTRING_AUTH = False
AWS_IS_GZIPPED = True
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME
CORS_ORIGIN_ALLOW_ALL = True
AWS_DEFAULT_ACL = "public-read"
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "ap-northeast-2")

CACHE_EXPIRATION_DURATION = 60 * 60 * 24

TESTING = False
DATA_UPLOAD_MAX_MEMORY_SIZE = 100000000
SITE_URL = "http://localhost:8000"
SITE_ID = 1

OLD_PASSWORD_FIELD_ENABLED = False

REQUEST_LOGGING_HTTP_4XX_LOG_LEVEL = logging.WARNING

DLFE_APP_NAME = "mmd"
DLFE_LOG_SENSITIVE_USER_DATA = True


REQUEST_LOGGING_ENABLE_COLORIZE = False
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

XRAY_RECORDER = {
    "AUTO_INSTRUMENT": True,
    "AWS_XRAY_CONTEXT_MISSING": "LOG_ERROR",
    "PLUGINS": ("ECSPlugin",),
    "SAMPLING": True,
    # the segment name for segments generated from incoming requests
    "AWS_XRAY_TRACING_NAME": "MMD API",
    "DYNAMIC_NAMING": "*",
}

SKIP_LOGGING_PATH = ["/api/healthcheck/"]


CORS_ALLOWED_ORIGIN_REGEXES = []
EVENT_BUS_PUSHOPS = "mmd-event-bus"

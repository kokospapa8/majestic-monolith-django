from aws_xray_sdk.core import xray_recorder
from .local import *

# TEST_DB_USER = get_env_variable("TEST_DB_USER")  # root
# TEST_DB_PASSWORD = get_env_variable("TEST_DB_PASSWORD")  # password
# TEST_DB_HOST = get_env_variable("TEST_DB_HOST")  # db
# TEST_DB_DATABASE_NAME = get_env_variable("TEST_DB_DATABASE_NAME")  # "daas_test"
# TEST_REDIS_HOST = get_env_variable("TEST_REDIS_HOST")
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": TEST_DB_DATABASE_NAME,
#         "USER": TEST_DB_USER,
#         "PASSWORD": TEST_DB_PASSWORD,
#         "HOST": TEST_DB_HOST,
#         "PORT": "3306",
#         "CONN_MAX_AGE": 3600,
#         "OPTIONS": {
#             "init_command": "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1, read_rnd_buffer_size=256000",
#             "charset": "utf8mb4",
#         },
#         "TEST": {"CHARSET": "utf8mb4", "COLLATION": "utf8mb4_unicode_ci"},
#     }
# }
#
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": f"redis://{TEST_REDIS_HOST}:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "IGNORE_EXCEPTION": True,  # needed for redis is only cache
#             "PARSER_CLASS": "redis.connection.HiredisParser",
#         },
#         "KEY_PREFIX": "test"
#
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'testdb.sqlite3',
    }
}
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon-default': '100/minute',
    'anon-burst': '100/minute',
    'anon-suppressed': '100/minute',
    'user-default': '100/minute',
    'user-burst': '100/minute',
    'user-suppressed': '100/minute',
    'auth-check': '30/minute',
    'sms-request': '30/minute',
}

ENV = "test"
ENV_ALIAS = ENV

AWS_LOCATION = "test"

TESTING = (ENV == "test")

# MIDDLEWARE.remove('aws_xray_sdk.ext.django.middleware.XRayMiddleware')
# INSTALLED_APPS.remove('aws_xray_sdk.ext.django')

XRAY_RECORDER = {
    'AUTO_INSTRUMENT': False,
    'AWS_XRAY_CONTEXT_MISSING': 'LOG_ERROR',
    'SAMPLING': False,
    # the segment name for segments generated from incoming requests
    'AWS_XRAY_TRACING_NAME': "MMD API"
}

xray_recorder.configure(sampling=False)

# STATIC
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = "/static/"
STATIC_ROOT = "/Users/jinwookbaek/Project/daas-server/static"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

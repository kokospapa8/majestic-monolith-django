# -*- coding: utf-8 -*-
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("core.authentication.DmmJWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
        "rest_framework_api_key.permissions.HasAPIKey",
    ],
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_PAGINATION_CLASS": "core.pagination.MMDPageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_THROTTLE_CLASSES": [
        "core.throttling.AnonDefaultThrottle",
        "core.throttling.UserDefaultThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon-default": "30/minute",
        "anon-burst": "120/minute",
        "anon-suppressed": "10/minute",
        "user-default": "60/minute",
        "user-burst": "120/minute",
        "user-suppressed": "10/minute",
        "auth-check": "30/minute",
        "sms-request": "10/minute",
    },
    "EXCEPTION_HANDLER": "core.exception_handler.custom_exception_handler",
}

OLD_PASSWORD_FILE_ENABLED = True
COERCE_DECIMAL_TO_STRING = False

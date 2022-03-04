# -*- coding: utf-8 -*-
from datetime import timedelta
ACCOUNT_AUTHENTICATION_METHOD = "username"

AUTHENTICATION_BACKENDS = (
    # "core.auth_backends.AuthenticationBackend",
    # "core.auth_backends.AppleAuthenticationBackend",
    "core.auth_backends.PasswordlessAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",

    # "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_EMAIL_REQUIRED = False

ACCOUNT_EMAIL_VERIFICATION = "optional"  # optional

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"

ACCOUNT_USERNAME_BLACKLIST = ["admin"]

ACCOUNT_USERNAME_MIN_LENGTH = 1

ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    # 'SIGNING_KEY': SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

ACCOUNT_ADAPTER = "auth.adapter.AuthAccountAdapter"

ACCOUNT_USERNAME_REQUIRED = True

USERPROFILE_FULLNAME_MAX_LENGTH = 32
USERPROFILE_FULLNAME_MIN_LENGTH = 2
# REST_AUTH_SERIALIZERS = {
#     'PASSWORD_RESET_SERIALIZER':'auth.serializers.PasswordResetNewFormSerializer'
# }

LOGIN_SERIALIZER = "auth.serializers.PhonenumberLoginSerializer"

ACCOUNT_AUTHENTICATION_METHOD = "username"

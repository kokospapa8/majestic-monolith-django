# -*- coding: utf-8 -*-
# This is application specific config

from pytz import timezone

OPS_ADMIN_EMAIL = ["example@example.com"]

EST_TIMEZONE = timezone('Asia/Seoul')

BYPASS_PHONENUMBER_REGEX = '\+821012341\d{3}'
PHONENUMBER_EXPIRATION = 3  # minutes
PHONENUMBER_DAILY_SIGNIN_LIMIT = 5
PHONENUMBER_VERIFICATION_TOKEN_LENGTH = 4

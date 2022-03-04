"""
Provides various throttling policies.
https://www.notion.so/Throttling-f316d0c4f8c445a78190fcb4caf27f94
"""

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AnonDefaultThrottle(AnonRateThrottle):
    scope = 'anon-default'


class AnonBurstThrottle(AnonRateThrottle):
    scope = 'anon-burst'


class AnonSuppressedThrottle(AnonRateThrottle):
    scope = 'anon-suppressed'


class UserDefaultThrottle(UserRateThrottle):
    scope = 'user-default'


class UserBurstThrottle(UserRateThrottle):
    scope = 'user-burst'


class UserSuppressedThrottle(UserRateThrottle):
    scope = 'user-suppressed'


class AuthCheckThrottle(AnonRateThrottle):
    scope = 'auth-check'


class SMSRequestThrottle(AnonRateThrottle):
    scope = 'sms-request'

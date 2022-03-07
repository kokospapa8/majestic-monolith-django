import datetime
import logging
import re


import jwt
from cryptography.hazmat.primitives import serialization  # pragma: no cover
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt.algorithms import RSAAlgorithm  # pragma: no cover

from core.utils import tokey

User = get_user_model()


def bypass_token_request(phonenumber):
    return bool(re.search(settings.BYPASS_PHONENUMBER_REGEX, phonenumber))


def is_banned_phonenumber(phonenumber):
    hashed_phonenumber = tokey(phonenumber.country_code, phonenumber.national_number)
    if User.objects.filter(phonenumber_meta=hashed_phonenumber).exists():
        return True


def get_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def get_dob_from_str(dob, fmt="%Y%m%d"):
    return datetime.datetime.strptime(dob, fmt)

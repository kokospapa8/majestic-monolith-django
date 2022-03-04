# -*- coding: utf-8 -*-
import datetime
import hashlib
import os
import random
import string
from typing import Tuple
from uuid import uuid4
import pytz

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache import caches
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text
from rest_framework.exceptions import ValidationError


def tokey(*args):
    def _encode(value, charset="utf-8", errors="ignore"):
        if isinstance(value, bytes):
            return value
        return value.encode(charset, errors)

    salt = "||".join([force_text(arg) for arg in args])
    hash_ = hashlib.md5(_encode(salt))
    return hash_.hexdigest()


@deconstructible
class UserPathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        # get filename
        now = str(datetime.datetime.now())

        if hasattr(instance, "user") and instance.user.username:
            key = tokey(instance.user.username, filename, now)
            filename = "{}.{}".format(key, ext)
        else:
            key = tokey(uuid4().hex, ext, now)
            filename = "{}.{}".format(key, ext)
        # return the whole relative path to the file
        return os.path.join(self.path, filename)


def invalidate_page_cache(page_cache_prefix):
    from django.core.cache.backends.locmem import LocMemCache
    cache = caches[settings.CACHE_MIDDLEWARE_ALIAS]
    if isinstance(cache, LocMemCache):
        for key in cache._cache.keys():
            if page_cache_prefix.replace("*", "") in key:
                del cache._cache[key]
    else:
        cache.delete_pattern(page_cache_prefix)


class DictObject(object):
    def __init__(self, dict_object):
        self._object = dict_object

    def __getattr__(self, attr):
        ret = self._object[attr]
        if type(ret) in [dict, list]:
            self._object[attr] = DictObject(ret)
            return ret
        return ret

    def __getitem__(self, key):
        ret = self._object[key]
        if type(ret) in [dict, list]:
            self._object[key] = DictObject(ret)
            return ret
        return ret


def create_random_string(max_length, letters=string.ascii_letters):
    return ''.join(random.choice(letters) for i in range(random.randint(1, max_length)))


def filter_users_by_phonenumber(phonenumber):
    User = get_user_model()
    users = list(User.objects.filter(phonenumber=phonenumber))
    return list(set(users))


def get_distance(lat1, lat2, lng1, lng2):
    from math import sin, cos, sqrt, atan2, radians
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lng1)
    lat2 = radians(lat2)
    lon2 = radians(lng2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def hash_string_for_seed(text, length=3):
    return int(hashlib.sha256(text.encode('utf-8')).hexdigest(), 16) % length


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def convert_empty_string_to_none(representation: dict) -> dict:
    def converter(i):
        if isinstance(i, str):
            return i or None
        return i

    for key, value in representation.items():
        representation[key] = converter(value)
    return representation


def clean_phonumber_for_national_str(phonenumber):
    from phonenumber_field.phonenumber import PhoneNumber
    phonenumber = phonenumber.replace("-", "")
    if isinstance(phonenumber, PhoneNumber):
        return f"0{phonenumber.national_number}"
    elif isinstance(phonenumber, str):
        if "+82" in phonenumber:
            return phonenumber.replace("+82", "0")
    return str(phonenumber)


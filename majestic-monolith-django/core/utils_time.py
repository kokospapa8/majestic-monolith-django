# -*- coding: utf-8 -*-
import datetime
import random
from typing import Tuple

import pytz
from django.utils import timezone
from rest_framework.exceptions import ValidationError


def get_local_today(timezone_string):
    try:
        user_timezone = pytz.timezone(timezone_string)
    except pytz.exceptions.UnknownTimeZoneError:
        raise ValidationError("Unknown Time Zone")
    local_date = timezone.now().astimezone(tz=user_timezone).date()
    return local_date, user_timezone


def generate_random_time(time_range: Tuple[int, int]) -> datetime.time:
    start_time, end_time = time_range
    random_hour = random.randint(start_time, end_time)
    random_minute = random.randint(0, 59)
    return datetime.time(random_hour, random_minute)


def datetime_to_local_time(dt, local_tz=None):
    dt = dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return dt

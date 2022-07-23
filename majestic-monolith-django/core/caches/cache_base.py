from django.conf import settings
from django.core.cache import cache, caches

DEFAULT_CACHE_ALIAS = "default"


def _get_cache(cache_alias):
    # did this because debug toolbar does not track caches when not using just cache.
    # So, caches["default"] is not tracked
    if cache_alias == DEFAULT_CACHE_ALIAS:
        return cache
    else:
        return caches[cache_alias]


class CacheBase:
    key_prefix = ""
    cache_alias = DEFAULT_CACHE_ALIAS
    single_key = False
    expire_duration = settings.CACHE_EXPIRATION_DURATION

    @classmethod
    def _set_default_key_prefix(cls):
        if cls.key_prefix == "":
            cls.key_prefix = cls.__name__

    def __init__(self):
        self.cache = _get_cache(self.cache_alias)

        self._set_default_key_prefix()

    def _format_key(self, key):
        if self.single_key:
            return self.key_prefix
        elif isinstance(key, tuple) or isinstance(key, list):
            return f'{self.key_prefix}:{"-".join(str(k) for k in key)}'
        else:
            return f"{self.key_prefix}:{key}"

    def _args_format_key_list(self, *args):
        return [self._format_key(key) for key in args]

    def cache_get(self, key):
        key = self._format_key(key)
        data = self.cache.get(key)
        return data

    def cache_get_many(self, *args):
        if self.single_key:
            return self.get(*args)
        else:
            key_list = self._args_format_key_list(*args)
            result = self.cache.get_many(key_list)
            missing = [key for key in args if self._format_key(key) not in result]
            return result, missing

    def cache_set(self, key, value, expire_duration=None):
        key = self._format_key(key)

        # implicit delete
        if value is None:
            self.delete(key)
        else:
            self.cache.set(key, value, expire_duration or self.expire_duration)

    def delete(self, key):
        key = self._format_key(key)
        self.cache.delete(key)

    def delete_many(self, *args):
        key_list = self._args_format_key_list(*args)
        self.cache.delete_many(key_list)

    def add(self, key, value):
        key = self._format_key(key)
        if not self.get(key):
            self.set(key, value)

    def delete_pattern(self, pattern):
        self.cache.delete_pattern(pattern)

    def delete_all(self):
        pattern = self._format_key("*")
        return self.delete_pattern(pattern)

    def incr(self, key, delta):
        key = self._format_key(key)
        self.cache.incr(key, delta)

    def decr(self, key, delta):
        key = self._format_key(key)
        self.cache.incr(key, -delta)


class NewBadgeCache(CacheBase):
    expire_duration = 60 * 60 * 24 * 30 * 6

    def get(self, user_uuid):
        return self.cache_get(user_uuid)

    def set(self, user_uuid, data):
        self.cache_set(user_uuid, data)


class SimpleGetCache(CacheBase):
    def get(self, key=None, force_db=False, *args, **kwargs):
        data = None

        if force_db:
            data = None
        else:
            data = self.cache_get(key)

        if data is None:
            data = self.get_from_db(key, *args, **kwargs)
            self.cache_set(key, data)
        return data

    def delete(self, key=None):
        key = self._format_key(key)
        self.cache.delete(key)

from core.caches import CacheBase


class PhonenumberVerificationCache(CacheBase):
    expire_duration = 60 * 60 * 24
    key_prefix = 'phonenumberverification'

    def incr(self, phonenumber, delta=1):
        key = self._format_key(phonenumber)
        try:
            self.cache.incr(key, delta)
        except ValueError:
            self.cache_set(phonenumber, 1)

    def get(self, phonenumber, *args, **kwargs):
        return self.cache_get(phonenumber)

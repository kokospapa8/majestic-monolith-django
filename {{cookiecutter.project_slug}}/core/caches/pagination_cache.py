from .cache_base import CacheBase


class PaginationCache(CacheBase):
    expire_duration = 60

    def __init__(self):
        super().__init__()

    def get_from_db(self, key, *args, **kwargs):
        raise NotImplementedError("get_from_db is not implemented.")

    def get_item(self, key):
        raise NotImplementedError("get_item is not implemented.")

    def get(self, key, page_num, page_size=50, *args, **kwargs):
        page_num = max(int(page_num), 1)
        page_size = max(int(page_size), 1)

        result = []

        uuid_list = self.cache_get(key)
        if uuid_list is None:
            uuid_list = self.get_from_db(key, *args, **kwargs)
            self.cache_set(key, uuid_list)

        start = page_size * (page_num - 1)
        end = start + page_size
        for uuid in uuid_list[start:end]:
            result.append(self.get_item(uuid))

        return result

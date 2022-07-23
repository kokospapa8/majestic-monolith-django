# -*- coding: utf-8 -*-
from django_redis.client import DefaultClient
from rediscluster import RedisCluster


class CustomRedisCluster(DefaultClient):
    def connect(self, index):
        """Override the connection retrival function."""
        return RedisCluster.from_url(self._server[index], skip_full_coverage_check=True)

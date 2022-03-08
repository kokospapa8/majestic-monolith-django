# -*- coding: utf-8 -*-
from django.conf import settings
from core.caches import ModelCacheBase, CacheBase

from .serializers import DistributionCenterSerializer
from .models import DistributionCenter


class DistributionCenterCache(ModelCacheBase):
    expire_duration = 60 * 60 * 24 * 30
    serializer_class = DistributionCenterSerializer
    key_prefix = 'center'

    def get_from_db(self, key, *args, **kwargs):
        try:
            address = DistributionCenter.objects.get(uuid=key)
            return address
        except DistributionCenter.DoesNotExist:
            return None

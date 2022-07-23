# -*- coding: utf-8 -*-

from core.caches import ModelCacheBase

from .models import DistributionCenter
from .serializers import DistributionCenterSerializer


class DistributionCenterCache(ModelCacheBase):
    expire_duration = 60 * 60 * 24 * 30
    serializer_class = DistributionCenterSerializer
    key_prefix = "center"

    def get_from_db(self, key, *args, **kwargs):
        try:
            center = DistributionCenter.objects.get(center_code=key)
            return center
        except DistributionCenter.DoesNotExist:
            return None

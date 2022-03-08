# -*- coding: utf-8 -*-
import json

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.http import Http404

from core.caches import ModelCacheBase, CacheBase, NewBadgeCache
from .utils_user import get_proxy_userprofile_model, get_proxy_userprofile_serializer

User = get_user_model()


class UserProfileCache(ModelCacheBase):
    expire_duration = 60 * 60 * 24
    serializer_class = None
    key_prefix = 'up'
    user_instance = None

    def get_serializer_class(self):

        return get_proxy_userprofile_serializer(self.user_instance)

    def get_from_db(self, key, *args, **kwargs):
        try:
            user = User.objects.get(uuid=key)
            self.user_instance = user
        except User.DoesNotExist:
            return None
        if not user.is_active:
            return None
        proxy_profile = get_proxy_userprofile_model(user)
        profile, created = proxy_profile.objects.select_related('user') \
            .get_or_create(user__uuid=key, defaults={'user': user})
        return profile

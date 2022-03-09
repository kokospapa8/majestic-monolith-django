# -*- coding: utf-8 -*-
import datetime
import logging

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from core.permissions import IsProfileOwner
from core.throttling import UserDefaultThrottle, UserBurstThrottle
from core.views import RetrievePatchOnlyAPIView
from user.serializers import UserProfileBaseSerializer

from .utils_user import get_proxy_userprofile_serializer, get_proxy_userprofile_model,\
    delete_user_profile_cache
from .docs import doc_user_self_get, doc_user_self_patch

User = get_user_model()

logger = logging.getLogger("django.eventlogger")


class UserSelfView(RetrievePatchOnlyAPIView):
    permission_classes = [permissions.IsAuthenticated & IsProfileOwner]
    serializer_class = UserProfileBaseSerializer

    def get_serializer_class(self):
        return get_proxy_userprofile_serializer(self.request.user)

    def get_throttles(self):
        if self.request.method == 'GET':
            self.throttle_classes = [UserBurstThrottle, ]
        elif self.request.method == 'PATCH':
            self.throttle_classes = [UserDefaultThrottle, ]
        return super().get_throttles()

    @doc_user_self_get
    def get(self, request, *args, **kwargs):
        from .caches import UserProfileCache
        profile_cache = UserProfileCache().get(request.user.uuid)
        return Response(profile_cache)

    @doc_user_self_patch
    def patch(self, request, *args, **kwargs):
        userprofile_model = get_proxy_userprofile_model(request.user)
        instance = userprofile_model.objects.get(user=request.user)
        serializer = self.get_serializer_class()(instance,
                                                 data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        delete_user_profile_cache(request.user.uuid)
        from .caches import UserProfileCache
        profile_cache = UserProfileCache().get(request.user.uuid)

        return Response(profile_cache)

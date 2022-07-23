# -*- coding: utf-8 -*-
import logging

from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response

from core.serializers import BlankSerializer


class FlushCacheView(GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = BlankSerializer
    authentication_classes = [SessionAuthentication]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def post(self, request, *args, **kwargs):
        from django.core.cache import cache

        cache.clear()
        return Response({"message": "cache flushed"}, status=status.HTTP_201_CREATED)


class Raise500View(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlankSerializer

    def post(self, request, *args, **kwargs):
        from user.models import CustomUser

        CustomUser.objects.filter(qwdqwd=1)
        return Response({})


class LoggerTest(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlankSerializer

    def get(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)
        print(__name__)  # noqa: T201
        logger.debug("general logger debug")
        logger.info("general logger info")
        logger.warning("general logger warning")
        logger.error("general logger error")

        debug_logger = logging.getLogger("django.debuglogger")
        debug_logger.debug("debug logger debug")
        debug_logger.info("debug logger info")
        debug_logger.warning("debug logger warning")

        event_logger = logging.getLogger("django.eventlogger")
        event_logger.debug("event logger debug")
        event_logger.info("event logger info")
        event_logger.warning("event logger warning")

        return Response({})

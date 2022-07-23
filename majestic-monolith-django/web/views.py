# -*- coding: utf-8 -*-
import logging

from django.http import HttpResponseRedirect
from rest_framework import permissions
from rest_framework.generics import GenericAPIView

logger = logging.getLogger("django.eventlogger")


class IndexRedirectView(GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # this is api server no need to pass query param
        return HttpResponseRedirect("https://www.youtube.com/watch?v=BOvxJaklcr0")

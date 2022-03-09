# -*- coding: utf-8 -*-
import logging

from rest_framework import serializers
from .models import DistributionCenter

logger = logging.getLogger("django.eventlogger")


class DistributionCenterSerializer(serializers.ModelSerializer):
    staff_names = serializers.SerializerMethodField()

    class Meta:
        model = DistributionCenter
        fields = ["uuid", "center_code", "name", "staff_names"]

    def get_staff_names(self, obj):
        # TODO user API
        from user.caches import UserProfileCache
        users = []
        uuid_list = obj.staff_members.get('uuid', [])
        for uuid in uuid_list:
            users.append(UserProfileCache().get(uuid))
        return "\n".join(f"{user['username']}" for user in users)

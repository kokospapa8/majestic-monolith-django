# -*- coding: utf-8 -*-
import logging

from rest_framework import serializers

from .models import DistributionCenter

logger = logging.getLogger("django.eventlogger")


class DistributionCenterSerializer(serializers.ModelSerializer):
    staff_members = serializers.SerializerMethodField()

    class Meta:
        model = DistributionCenter
        fields = ["uuid", "center_code", "name", "staff_members"]

    def get_staff_members(self, obj):
        # TODO user services
        from user.caches import UserProfileCache

        users = []
        uuid_list = obj.staff_members.get("uuid", [])
        for uuid in uuid_list:
            users.append(UserProfileCache().get(uuid))
        return users

    def update(self, instance, validated_data):
        name = validated_data.get("name", None)
        if name:
            instance.name = name
            instance.save()
        return instance

# -*- coding: utf-8 -*-
import logging

from django.contrib import admin
from .models import DistributionCenter

logger = logging.getLogger(__name__)


@admin.register(DistributionCenter)
class DistributionCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'center_code', 'uuid', 'staff_member_names']
    search_fields = ['=name', "=center_code"]
    readonly_fields = ['uuid']

    def staff_member_names(self, obj):
        from user.caches import UserProfileCache
        users = []
        uuid_list = obj.staff_members.get('uuid', [])
        for uuid in uuid_list:
            users.append(UserProfileCache().get(uuid))
        return "\n".join(f"{user['username']}" for user in users)

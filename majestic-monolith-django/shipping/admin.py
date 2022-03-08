# -*- coding: utf-8 -*-
import logging

from django.contrib import admin

from daterangefilter.filters import PastDateRangeFilter, FutureDateRangeFilter

from .models import ShippingItem, ShippingBatch, ShippingTransport
from .choices import ShippingItemStatus

logger = logging.getLogger(__name__)


@admin.register(ShippingItem)
class ShippingItemAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'tracking_number', 'sku', 'status',
                    'current_distribution_center_code',
                    'timestamp_created', 'timestamp_completed']
    raw_id_fields = ['shipping_batches', ]
    search_fields = ['=tracking_number', "=sku"]
    list_filter = ['status',
                   ('timestamp_created', PastDateRangeFilter),
                   ('timestamp_completed', PastDateRangeFilter)]
    readonly_fields = ['uuid']
    actions = ['reset_status']

    date_hierarchy = 'timestamp_created'

    @admin.action(description='reset shipping item data')
    def reset_status(self, request, queryset):
        queryset.update(status=ShippingItemStatus.CREATED)
        for item in queryset:
            item.shipping_batches.clear()


@admin.register(ShippingBatch)
class ShippingBatchAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'alias', 'completed',
                    'transport_assigned',
                    'timestamp_created', 'timestamp_completed']
    raw_id_fields = ['shipping_transport', ]
    search_fields = ['=alias', ]
    list_filter = ['completed',
                   ('timestamp_created', PastDateRangeFilter),
                   ('timestamp_completed', PastDateRangeFilter)]
    readonly_fields = ['uuid']


@admin.register(ShippingTransport)
class ShippingTransportAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'completed',
                    'distribution_center_code_source',
                    'distribution_center_code_destination',
                    'driver'
                    'timestamp_created',
                    'timestamp_departed',
                    'timestamp_arrived']
    list_filter = ['completed',
                   ('timestamp_created', PastDateRangeFilter),
                   ('timestamp_departed', PastDateRangeFilter),
                   ('timestamp_arrived', PastDateRangeFilter)]

    def driver(self, obj):
        # get user
        return None
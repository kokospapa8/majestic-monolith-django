import logging

from rest_framework import serializers
from .models import ShippingItem, ShippingBatch, ShippingTransport

logger = logging.getLogger("django.eventlogger")


class ShippingTransportSerializer(serializers.ModelSerializer):
    distribution_center_source = serializers.SerializerMethodField()
    distribution_center_destination = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()

    class Meta:
        model = ShippingTransport
        fields = ["uuid", "completed",
                  "distribution_center_source",
                  "distribution_center_destination",
                  "driver",
                  "timestamp_created",
                  "timestamp_departed",
                  "timestamp_arrived"]

    def get_distribution_center_source(self, obj):
        # TODO get from application service
        from distribution.caches import DistributionCenterCache
        return DistributionCenterCache().get(obj.distribution_center_code_source)

    def get_distribution_center_destination(self, obj):
        # TODO get from application service
        from distribution.caches import DistributionCenterCache
        return DistributionCenterCache().get(obj.distribution_center_code_destination)

    def get_driver(self, obj):
        # TODO get from application service
        from user.caches import UserProfileCache
        return UserProfileCache().get(obj.driver_uuid)


class ShippingBatchSerializer(serializers.ModelSerializer):
    shipping_transport = ShippingTransportSerializer()

    class Meta:
        model = ShippingBatch
        fields = ["uuid", "alias", "completed", "shipping_transport",
                  "timestamp_created", "timestamp_completed"]


class ShippingItemSerializer(serializers.ModelSerializer):
    shipping_batches_history = serializers.SerializerMethodField()
    tracking_number = serializers.CharField(read_only=True)
    current_distribution_center_code = serializers.CharField(read_only=True,
                                                             help_text="change only by transport api")

    class Meta:
        model = ShippingItem
        fields = ["uuid", "tracking_number", "sku", "status",
                  "shipping_batches_history", "current_distribution_center_code",
                  "timestamp_created", "timestamp_completed"]

    def get_shipping_batches_history(self, obj):
        return obj.shipping_batches.select_related('shipping_transport').all().\
            order_by('-timestamp_created').values('alias', 'completed',
                                                  'shipping_transport__uuid',
                                                  'shipping_transport__distribution_center_code_source',
                                                  'shipping_transport__distribution_center_code_destination',
                                                  )

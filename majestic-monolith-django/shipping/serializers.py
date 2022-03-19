import logging

from rest_framework import serializers

from .models import ShippingItem, ShippingBatch, ShippingTransport
from .services import ShippingDTO, ShippingBatchService, \
    ShippingItemService, TransportService
from .choices import ShippingItemStatus
from .exceptions import ShippingTransportCompletedException, \
    ShippingTransportBatchNotExistException, \
    ShippingTransportBatchAlreadyCompletedException, \
    ShippingBatchCompletedException, ShippingBatchItemAlreadyExsitException, \
    ShippingBatchItemAddInvalidStatusException, \
    ShippingTransportDistributionNotConfiguredException, \
    ShippingTransportDriverNotConfiguredException, \
    ShippingTransportNoBatchException, ShippingTransportNotDepartedException

logger = logging.getLogger("django.eventlogger")


class ShippingTransportSerializer(serializers.ModelSerializer):
    distribution_center_source = serializers.SerializerMethodField()
    distribution_center_destination = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()
    distribution_center_code_source = serializers.CharField(write_only=True)
    distribution_center_code_destination = serializers.CharField(write_only=True)

    class Meta:
        model = ShippingTransport
        fields = ["uuid", "completed", "batch_count",
                  "distribution_center_source",
                  "distribution_center_destination",
                  "distribution_center_code_source",
                  "distribution_center_code_destination",
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
    shipping_transport = ShippingTransportSerializer(required=False)

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


class ShippingBatchAddSerializer(serializers.Serializer):
    alias = serializers.CharField(max_length=20, required=True)

    def validate(self, attrs):
        alias = attrs['alias']
        transport = self.context['transport']

        if transport.completed:
            raise ShippingTransportCompletedException()
        try:
            batch = ShippingBatch.objects.get(alias=alias)
            self.context['batch'] = batch
        except ShippingBatch.DoesNotExist:
            raise ShippingTransportBatchNotExistException()
        if batch.completed:
            raise ShippingTransportBatchAlreadyCompletedException()
        return attrs

    def save(self):
        shipping_dto = ShippingDTO(batch=self.context['batch'],
                                   transport=self.context['transport'])
        ShippingBatchService(shipping_dto).add_to_transport()
        return self.context['batch']

    def to_representation(self, instance):
        # TODO: cache
        serializer = ShippingBatchSerializer(self.context['batch'])
        return serializer.data


class ShippingItemAddSerializer(serializers.Serializer):
    tracking_number = serializers.CharField(max_length=20, required=True)

    def validate(self, attrs):
        tracking_number = attrs['tracking_number']
        batch = self.context['batch']

        if batch.completed:
            raise ShippingBatchCompletedException()
        try:
            shippingitem = ShippingItem.objects.get(tracking_number=tracking_number)
            self.context['shippingitem'] = shippingitem
        except ShippingItem.DoesNotExist:
            raise ShippingBatchItemAlreadyExsitException()
        if shippingitem.status not in [ShippingItemStatus.CREATED,
                                       ShippingItemStatus.MOVING]:
            raise ShippingBatchItemAddInvalidStatusException()
        return attrs

    def save(self):
        shipping_dto = ShippingDTO(batch=self.context['batch'],
                                   item=self.context['shippingitem'])
        ShippingItemService(shipping_dto).add_to_batch()
        return self.context['batch']

    def to_representation(self, instance):
        # TODO: cache
        serializer = ShippingItemSerializer(self.context['shippingitem'])
        return serializer.data


class ShippingTransportStartSerializer(serializers.Serializer):
    driver_uuid = serializers.UUIDField(required=False, write_only=True)

    def validate(self, attrs):
        transport = self.context['transport']
        driver_uuid = attrs.get('driver_uuid', None)
        if transport.completed:
            raise ShippingTransportCompletedException()
        if not (transport.distribution_center_code_source
                and transport.distribution_center_code_destination):
            raise ShippingTransportDistributionNotConfiguredException()
        if ShippingBatch.objects.filter(shipping_transport=transport).count() == 0:
            raise ShippingTransportNoBatchException()
        if not transport.driver_uuid and not driver_uuid:
            raise ShippingTransportDriverNotConfiguredException()

        return attrs

    def save(self):
        transport = self.context['transport']
        shipping_dto = ShippingDTO(transport=transport)
        TransportService(shipping_dto).transport_start(
            self.data.get('driver_uuid', None))
        return transport

    def to_representation(self, instance):
        # TODO: cache
        serializer = ShippingTransportSerializer(self.context['transport'])
        return serializer.data


class ShippingTransportCompleteSerializer(serializers.Serializer):
    def validate(self, attrs):
        transport = self.context['transport']
        if transport.timestamp_departed is None:
            raise ShippingTransportNotDepartedException()
        if transport.completed:
            raise ShippingTransportCompletedException()
        return attrs

    def save(self):
        transport = self.context['transport']
        shipping_dto = ShippingDTO(transport=transport)
        TransportService(shipping_dto).transport_complete()
        return transport

    def to_representation(self, instance):
        # TODO: cache
        serializer = ShippingTransportSerializer(self.context['transport'])
        return serializer.data

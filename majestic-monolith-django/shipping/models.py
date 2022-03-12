import uuid
import logging

from django.db import models
from django.db import IntegrityError

from .choices import ShippingItemStatus
from .utils_shipping import generate_batch_alias, generate_tracking_number

logger = logging.getLogger("django.eventlogger")


class ShippingItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    tracking_number = models.CharField(
        default=generate_tracking_number,
        max_length=20, unique=True, blank=True,
        editable=False, db_index=True)
    sku = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=24, choices=ShippingItemStatus.choices,
                              blank=True, default=ShippingItemStatus.CREATED, db_index=True)

    shipping_batches = models.ManyToManyField(
        "shipping.ShippingBatch", blank=True, help_text='can assign multiple shipping batches')
    current_distribution_center_code = models.CharField(blank=True, null=True, max_length=16,
                                                        help_text="No FK since it's in different domain")
    timestamp_created = models.DateTimeField(null=True, blank=True,
                                             db_index=True, auto_now_add=True)
    timestamp_completed = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "shipping"
        db_table = "shipping_shippingitem"

    def __str__(self):
        return f"[ShippingItem:{self.sku}]{self.tracking_number} - {self.status}"

    def is_available_for_batch(self) -> bool:
        return not self.shipping_batches.filter(completed=False).exists()


class ShippingBatch(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    alias = models.CharField(default=generate_batch_alias, unique=True, max_length=20)
    completed = models.BooleanField(default=False, db_index=True)

    shipping_transport = models.ForeignKey("shipping.ShippingTransport", on_delete=models.PROTECT,
                                           null=True, blank=True, help_text="assigned to single transport")

    timestamp_created = models.DateTimeField(null=True, blank=True,
                                             db_index=True, auto_now_add=True)
    timestamp_transport_assigned = models.DateTimeField(null=True, blank=True)
    timestamp_completed = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "shipping"
        db_table = "shipping_shippingbatch"

    @property
    def transport_assigned(self) -> bool:
        return self.shipping_transport is not None

    def item_count(self) -> int:
        return ShippingItem.objects.filter(shipping_batches=self).count()

    @staticmethod
    def static_method():
        pass

    def __str__(self):
        return f"[ShippingBatch]{self.alias}"


class ShippingTransport(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    completed = models.BooleanField(default=False, db_index=True)

    distribution_center_code_source = models.CharField(blank=True, null=True,
                                                       max_length=16,
                                                       help_text="No FK since it's in different domain")
    distribution_center_code_destination = models.CharField(blank=True, null=True,
                                                            max_length=16,
                                                            help_text="No FK since it's in different domain")
    driver_uuid = models.UUIDField(blank=True, null=True,
                                    help_text="user_id, No FK since it's in different domain")

    timestamp_created = models.DateTimeField(null=True, blank=True,
                                             db_index=True, auto_now_add=True)
    timestamp_departed = models.DateTimeField(null=True, blank=True, db_index=True)
    timestamp_arrived = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        app_label = "shipping"
        db_table = "shipping_shippingtransport"

    def batch_count(self) -> int:
        return ShippingBatch.objects.filter(shipping_transport=self).count()

    def save(self, *args, **kwargs):
        # raise integrty error on same source and destination
        if self.distribution_center_code_source == \
                self.distribution_center_code_destination:
            logger.error(f"ShippingTransport: source and destination code cannot be same."
                         f"{self.distribution_center_code_source} -> "
                         f"{self.distribution_center_code_destination}")
            raise IntegrityError(f"ShippingTransport: source and destination code cannot be same.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[ShippingTransport]{self.uuid} " \
            f"{self.distribution_center_code_source} -> " \
            f"{self.distribution_center_code_destination}"

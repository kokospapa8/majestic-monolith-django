from dataclasses import dataclass

from django.utils import timezone

from core.services import DomainService

from .choices import ShippingItemStatus
from .events import ShippingEventsEmitter
from .models import ShippingBatch, ShippingItem, ShippingTransport


@dataclass
class ShippingDTO:
    item: ShippingItem = None
    batch: ShippingBatch = None
    transport: ShippingTransport = None


class ShippingBatchService(DomainService):
    dto: ShippingDTO

    def add_to_transport(self) -> ShippingBatch:
        batch = self.dto.batch
        batch.shipping_transport = self.dto.transport
        batch.timestamp_transport_assigned = timezone.now()
        batch.save()

        ShippingEventsEmitter().batch_added_to_transport(
            {"transport_uuid": self.dto.transport.uuid.hex, "batch_alias": batch.alias}
        )
        return batch


class ShippingItemService(DomainService):
    dto: ShippingDTO

    def add_to_batch(self) -> ShippingItem:
        item = self.dto.item
        item.shipping_batches.add(self.dto.batch)
        if item.status == ShippingItemStatus.CREATED:
            item.status = ShippingItemStatus.MOVING
        item.save()
        ShippingEventsEmitter().item_added_to_batch(
            {
                "item_tracking_number": item.tracking_number,
                "batch_alias": self.dto.batch.alias,
            }
        )
        return item


class TransportService(DomainService):
    dto: ShippingDTO

    def transport_start(self, driver_uuid=None) -> None:
        transport = self.dto.transport
        if driver_uuid:
            transport.driver_uuid = driver_uuid
        transport.timestamp_departed = timezone.now()
        transport.save()

    def transport_complete(self) -> None:
        transport = self.dto.transport

        qs_batches = ShippingBatch.objects.filter(shipping_transport=transport)
        qs_batches.update(completed=True, timestamp_completed=timezone.now())

        ShippingItem.objects.filter(shipping_batches__in=qs_batches).update(
            current_distribution_center_code=transport.distribution_center_code_destination
        )

        transport.timestamp_arrived = timezone.now()
        transport.save()

        ShippingEventsEmitter().transport_complete(
            {"transport_uuid": transport.uuid.hex}
        )


batch_service = ShippingBatchService()
shippingitem_service = ShippingItemService()
transport_service = TransportService()

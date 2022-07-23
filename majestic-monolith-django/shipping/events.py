import logging

from core.events import BaseEventsEmitter

logger = logging.getLogger("django.eventlogger")


class ShippingEventsEmitter(BaseEventsEmitter):
    SOURCE = "mmd.api.shipping"
    DIRECT_NOTIFICATION = True

    def batch_added_to_transport(self, data):
        kwargs = {"event_name": "BatchAddedToTransport", "params": {"data": data}}
        self.emit_eventbridge(**kwargs)

    def item_added_to_batch(self, data):
        kwargs = {"event_name": "ItemAddedToBatch", "params": {"data": data}}
        self.emit_eventbridge(**kwargs)

    def transport_complete(self, data):
        kwargs = {"event_name": "TransportComplete", "params": {"data": data}}
        self.emit_eventbridge(**kwargs)

from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import (
    ShippingTransportViewSet,
    ShippingBatchViewSet,
    ShippingItemViewSet,

    TransportBatchesView,
    BatchShippingitemsView
)

router_shippingitem = DefaultRouter()
router_shippingitem.register(r'shippingitems', ShippingItemViewSet, basename='shippingitem')

router_batch = DefaultRouter()
router_batch.register(r'batches', ShippingBatchViewSet, basename='batch')

router_transport = DefaultRouter()
router_transport.register(r'transports', ShippingTransportViewSet, basename='transport')

urlpatterns = [
    # shppingitem add to batch
    # shippingbatch add to transport

    # transport / batches
    path("transports/<uuid:uuid>/batches/", TransportBatchesView.as_view(), name="transport_batches"),
    path("batches/<str:alias>/shippingitems/", BatchShippingitemsView.as_view(), name="batch_shippingitems"),

]

urlpatterns += router_shippingitem.urls
urlpatterns += router_batch.urls
urlpatterns += router_transport.urls

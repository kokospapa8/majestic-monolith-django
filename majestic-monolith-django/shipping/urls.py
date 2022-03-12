from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import (
    ShippingTransportViewSet,
    ShippingBatchViewSet,
    ShippingItemViewSet,

    TransportBatchesView,
    TransportBatchesAddView,
    TransportStartView,
    TransportCompleteView,

    BatchShippingitemsView,
    BatchShippingitemsAddView
)

router_shippingitem = DefaultRouter()
router_shippingitem.register(r'shippingitems', ShippingItemViewSet, basename='shippingitem')

router_batch = DefaultRouter()
router_batch.register(r'batches', ShippingBatchViewSet, basename='batch')

router_transport = DefaultRouter()
router_transport.register(r'transports', ShippingTransportViewSet, basename='transport')

urlpatterns = [
    # transport
    path("transports/<uuid:uuid>/batches/", TransportBatchesView.as_view(), name="transport_batches"),
    path("transports/<uuid:uuid>/add/", TransportBatchesAddView.as_view(), name="transport_batches_add"),
    path("transports/<uuid:uuid>/start/", TransportStartView.as_view(), name="transport_batches_complete"),
    path("transports/<uuid:uuid>/complete/", TransportCompleteView.as_view(), name="transport_batches_complete"),

    # batches
    path("batches/<str:alias>/shippingitems/", BatchShippingitemsView.as_view(), name="batch_shippingitems"),
    path("batches/<str:alias>/add/", BatchShippingitemsAddView.as_view(), name="batch_shippingitem_add"),

]

urlpatterns += router_shippingitem.urls
urlpatterns += router_batch.urls
urlpatterns += router_transport.urls

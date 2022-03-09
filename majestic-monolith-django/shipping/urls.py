from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import (
    ShippingTransportViewSet,
    ShippingBatchViewSet,
    ShippingItemViewSet
)

router_shippingitem = DefaultRouter()
router_shippingitem.register(r'shippingitem', ShippingItemViewSet, basename='shippingitem')

router_batch = DefaultRouter()
router_batch.register(r'batch', ShippingBatchViewSet, basename='batch')

router_transport = DefaultRouter()
router_transport.register(r'transport', ShippingTransportViewSet, basename='transport')

urlpatterns = [
    # shppingitem add to batch
    # shippingbatch add to transport

    # transport / batches
    # batch/items
]

urlpatterns += router_shippingitem.urls
urlpatterns += router_batch.urls
urlpatterns += router_transport.urls

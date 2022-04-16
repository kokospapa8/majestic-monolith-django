from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import (
    DistributionCenterViewSet
)

router_center = DefaultRouter()
router_center.register(r'centers', DistributionCenterViewSet, basename='center')


urlpatterns = [
]

urlpatterns += router_center.urls

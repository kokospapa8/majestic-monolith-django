from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from .models import DistributionCenter
from .serializers import DistributionCenterSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Distribution Center",
        description="list all distribution center",
        tags=["distribution"],
    ),
    create=extend_schema(
        summary="Create a Shipping Distribution Center",
        description="create a distribution center",
        tags=["distribution"],
    ),
    retrieve=extend_schema(
        summary="Get a Shipping Distribution Center",
        description="get a distribution center by uuid",
        tags=["distribution"],
    ),
    destroy=extend_schema(
        summary="Delete a Shipping Distribution Center",
        description="delete a distribution center",
        tags=["distribution"],
    ),
    partial_update=extend_schema(
        summary="Update a Shipping Distribution Center",
        description="update a distribution center",
        tags=["distribution"],
    ),
)
class DistributionCenterViewSet(viewsets.ModelViewSet):
    serializer_class = DistributionCenterSerializer
    queryset = DistributionCenter.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["center_code", "name"]
    lookup_field = "uuid"

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from .models import DistributionCenter
from .serializers import DistributionCenterSerializer


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

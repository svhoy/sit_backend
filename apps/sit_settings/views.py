# pylint: disable=too-many-ancestors
from rest_framework import permissions, viewsets

from .models import UwbDeviceSettings
from .premissions import IsOwnerOrReadOnly
from .serializers import UwbDeviceSettingsSerializer


class SettingsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """

    queryset = UwbDeviceSettings.objects.all().order_by("id")
    serializer_class = UwbDeviceSettingsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

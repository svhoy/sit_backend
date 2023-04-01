from rest_framework import mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import DeviceTestGroups, DeviceTests, DistanceMeasurement
from .premissions import IsOwnerOrReadOnly
from .serializers import (
    DeviceTestGroupsSerializer,
    DeviceTestsSerializer,
    DistanceMeasurementSerializer,
)


class DistanceMeasurementViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    This viewset automatically provides `list` and `destroy` actions.
    """

    queryset = DistanceMeasurement.objects.all().order_by("-created")
    serializer_class = DistanceMeasurementSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    PageNumberPagination.page_size = 10
    PageNumberPagination.page_size_query_param = "size"


class DeviceTestGroupsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """

    queryset = DeviceTestGroups.objects.all().order_by("-created")
    serializer_class = DeviceTestGroupsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    PageNumberPagination.page_size = 10
    PageNumberPagination.page_size_query_param = "size"


class DeviceTestsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """

    queryset = DeviceTests.objects.all().order_by("-created")
    serializer_class = DeviceTestsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    PageNumberPagination.page_size = 10
    PageNumberPagination.page_size_query_param = "size"

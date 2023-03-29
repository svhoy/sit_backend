from rest_framework import mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import (
    DistanceMeasurement,
    MeasurementTest,
    MeasurementTestSettings,
)
from .premissions import IsOwnerOrReadOnly
from .serializers import (
    DistanceMeasurementSerializer,
    MeasurementTestSerializer,
    MeasurementTestSettingsSerializer,
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

    queryset = DistanceMeasurement.objects.all().order_by("created")
    serializer_class = DistanceMeasurementSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    PageNumberPagination.page_size = 10
    PageNumberPagination.page_size_query_param = "size"


class MeasurementTestSettingsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """

    queryset = MeasurementTestSettings.objects.all().order_by("created")
    serializer_class = MeasurementTestSettingsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    PageNumberPagination.page_size = 10
    PageNumberPagination.page_size_query_param = "size"


class MeasurementTestViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """

    queryset = MeasurementTest.objects.all().order_by("created")
    serializer_class = MeasurementTestSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    PageNumberPagination.page_size = 10
    PageNumberPagination.page_size_query_param = "size"

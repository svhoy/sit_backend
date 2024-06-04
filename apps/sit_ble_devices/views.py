# pylint: disable=too-many-ancestors
from rest_framework import mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import (
    AntDelay,
    Calibration,
    CalibrationsDistances,
    DeviceTestGroups,
    DeviceTests,
    DistanceMeasurement,
    UwbDevice,
)
from .premissions import IsOwnerOrReadOnly
from .serializers import (
    AntDelaySerializer,
    CalibrationsDistancesSerializer,
    CalibrationSerializer,
    DeviceTestGroupsSerializer,
    DeviceTestsSerializer,
    DistanceMeasurementSerializer,
    UwbDeviceSerializer,
)


class CalibrationsDistancesViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    This viewset automatically provides `list` actions.
    """

    serializer_class = CalibrationsDistancesSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = CalibrationsDistances.objects.all().order_by("created")
        calibration_id = self.request.query_params.get("calibration", None)
        if calibration_id is not None:
            queryset = queryset.filter(calibration_mod__id=calibration_id)
        return queryset


class CalibrationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    This viewset automatically provides `list`, `retrieve`,
    `update` and `destroy` actions.

    """

    queryset = Calibration.objects.all().order_by("-created")
    serializer_class = CalibrationSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    PageNumberPagination.page_size = 10
    PageNumberPagination.page_size_query_param = "size"


class UwbDeviceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """

    queryset = UwbDevice.objects.all().order_by("created")
    serializer_class = UwbDeviceSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    PageNumberPagination.page_size = 10
    PageNumberPagination.page_size_query_param = "size"


class AntDelayViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """

    queryset = AntDelay.objects.all().order_by("-created")
    serializer_class = AntDelaySerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    PageNumberPagination.page_size = 1000
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


class DistanceMeasurementViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    This viewset automatically provides `list` and `destroy` actions.
    """

    serializer_class = DistanceMeasurementSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    PageNumberPagination.page_size = 10
    PageNumberPagination.page_size_query_param = "size"

    def get_queryset(self):
        queryset = DistanceMeasurement.objects.all().order_by("-created")
        test_id = self.request.query_params.get("test", None)
        if test_id is not None:
            queryset = queryset.filter(test__id=test_id)
        return queryset

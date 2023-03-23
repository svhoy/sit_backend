from rest_framework import mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import DistanceMeasurement
from .serializers import DistanceMeasurementSerializer


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
    PageNumberPagination.page_size = 100
    PageNumberPagination.page_size_query_param = "size"

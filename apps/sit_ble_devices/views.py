from rest_framework import permissions, viewsets

from .models import DistanceMeasurement
from .serializers import DistanceMeasurementSerializer


class DistanceMeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = DistanceMeasurement.objects.all().order_by("created")
    serializer_class = DistanceMeasurementSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

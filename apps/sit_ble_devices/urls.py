from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views

from .views import DistanceMeasurementViewSet

app_name = "sit_ble_devices"

measurement_list = DistanceMeasurementViewSet.as_view({"get": "list"})
measurement_delete = DistanceMeasurementViewSet.as_view(
    {
        "delete": "destroy",
    }
)


urlpatterns = format_suffix_patterns(
    [
        path(
            "api/measurement-list/", measurement_list, name="measurement-list"
        ),
        path(
            "api/measurement-list/<int:pk>/",
            measurement_delete,
            name="measurement-detail",
        ),
    ]
)

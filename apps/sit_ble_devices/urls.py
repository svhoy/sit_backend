from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views

from .views import (
    DistanceMeasurementViewSet,
    MeasurementTestSettingsViewSet,
    MeasurementTestViewSet,
)

app_name = "sit_ble_devices"

measurement_list = DistanceMeasurementViewSet.as_view({"get": "list"})
measurement_delete = DistanceMeasurementViewSet.as_view(
    {
        "delete": "destroy",
    }
)
test_view_list = MeasurementTestViewSet.as_view(
    {"get": "list", "post": "create"}
)
test_settings_view_list = MeasurementTestSettingsViewSet.as_view(
    {"get": "list", "post": "create"}
)
test_settings_view_detail = MeasurementTestSettingsViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
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
        path("api/tests/", test_view_list, name="test-list"),
        path(
            "api/tests/settings-list",
            test_settings_view_list,
            name="test-settings-list",
        ),
        path(
            "api/tests/settings/<int:pk>/",
            test_settings_view_detail,
            name="test-settings-detail",
        ),
    ]
)

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    UwbDeviceViewSet,
    DeviceTestGroupsViewSet,
    DeviceTestsViewSet,
    DistanceMeasurementViewSet,
)

app_name = "sit_ble_devices"

device_detail = UwbDeviceViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)
device_list = UwbDeviceViewSet.as_view({"get": "list", "post": "create"})
measurement_list = DistanceMeasurementViewSet.as_view({"get": "list"})
measurement_delete = DistanceMeasurementViewSet.as_view(
    {
        "delete": "destroy",
    }
)
test_view_list = DeviceTestsViewSet.as_view({"get": "list", "post": "create"})
test_view_details = DeviceTestsViewSet.as_view(
    {
        "get": "retrieve",
        "delete": "destroy",
    }
)
test_groups_view_list = DeviceTestGroupsViewSet.as_view(
    {"get": "list", "post": "create"}
)
test_groups_view_detail = DeviceTestGroupsViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)


urlpatterns = format_suffix_patterns(
    [
        path("api/device/", device_list, name="device-list"),
        path(
            "api/device/<int:pk>/",
            device_detail,
            name="device-detail",
        ),
        path(
            "api/measurement-list/", measurement_list, name="measurement-list"
        ),
        path(
            "api/measurement-list/<int:pk>/",
            measurement_delete,
            name="measurement-detail",
        ),
        path("api/tests/", test_view_list, name="test-list"),
        path("api/tests/<int:pk>/", test_view_details, name="test-details"),
        path(
            "api/tests/groups",
            test_groups_view_list,
            name="test-groups-list",
        ),
        path(
            "api/tests/groups/<int:pk>/",
            test_groups_view_detail,
            name="test-groups-detail",
        ),
    ]
)

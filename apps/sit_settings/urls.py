# Third Party
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import SettingsViewSet


app_name = "sit_settings"


settings_list = SettingsViewSet.as_view({"get": "list", "post": "create"})
settings_detail = SettingsViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = format_suffix_patterns(
    [
        path("api/settings/uwb/", settings_list, name="uwbdevicesettings-list"),
        path(
            "api/settings/uwb/<int:pk>/",
            settings_detail,
            name="uwbdevicesettings-detail",
        ),
    ]
)

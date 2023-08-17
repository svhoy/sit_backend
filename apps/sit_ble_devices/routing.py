# Third Party
from django.urls import re_path

from .adapters import consumers

websocket_urlpatterns = [
    re_path(
        r"^ws/sit/(?P<room_id>\w+)$", consumers.BleDeviceConsumer.as_asgi()
    ),
]

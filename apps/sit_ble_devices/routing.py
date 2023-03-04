# Third Party
from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(r"ws/ble-devices/", consumers.BleDeviceConsumer.as_asgi()),
]

# Third Party
from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(r"ws/ble-scan/", consumers.BleScanConsumer.as_asgi())
]

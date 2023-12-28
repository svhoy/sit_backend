"""
ASGI config for sit_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

# Standard Library
import os

# Third Party
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack

from channels.layers import get_channel_layer

# Library
import apps.sit_ble_devices.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

django_asgi_app = get_asgi_application()
channel_layer = get_channel_layer()
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddlewareStack(
            URLRouter(
                apps.sit_ble_devices.routing.websocket_urlpatterns,
            )
        ),
        "channel": channel_layer,
    }
)

# Add the Celery worker to the ASGI application.

application_cl = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter([]),
    }
)

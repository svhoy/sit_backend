# pylint: disable=too-many-ancestors
from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer, UserSerializer

User = get_user_model()


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):  # pylint: disable=redefined-builtin
    return Response(
        {
            "token": reverse(
                "web:token_obtain_pair", request=request, format=format
            ),
            "users": reverse("web:user-list", request=request, format=format),
            "distance_measurements": reverse(
                "sit_ble_devices:measurement-list",
                request=request,
                format=format,
            ),
            "test": reverse(
                "sit_ble_devices:test-list",
                request=request,
                format=format,
            ),
            "test_groups": reverse(
                "sit_ble_devices:test-groups-list",
                request=request,
                format=format,
            ),
            "settings": reverse(
                "sit_settings:uwbdevicesettings-list",
                request=request,
                format=format,
            ),
        }
    )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

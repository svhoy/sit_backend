# Third Party
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views

from .views import MyTokenObtainPairView, UsersViewSet, api_root


app_name = "web"

user_list = UsersViewSet.as_view({"get": "list"})
user_detail = UsersViewSet.as_view({"get": "retrieve"})

urlpatterns = format_suffix_patterns(
    [
        path("api/", api_root, name="api-root"),
        path("api/users/", user_list, name="user-list"),
        path("api/users/<int:pk>/", user_detail, name="user-detail"),
        path(
            "api/token/",
            MyTokenObtainPairView.as_view(),
            name="token_obtain_pair",
        ),
        path(
            "api/token/refresh/",
            jwt_views.TokenRefreshView.as_view(),
            name="token_refresh",
        ),
    ]
)

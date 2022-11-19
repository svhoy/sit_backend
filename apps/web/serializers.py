# Third Party
from django.contrib.auth.models import Group, User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...

        return token


class UserSerializer(serializers.HyperlinkedModelSerializer):
    settings = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="sit_settings:uwbdevicesettings-detail",
        read_only=True,
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="web:user-detail",
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "settings"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

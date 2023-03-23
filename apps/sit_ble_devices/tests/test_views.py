# Third Party
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
@pytest.mark.django_db
def user_data():
    email = "test@example.com"
    username = "test"
    password = "1test23"
    user = User.objects.create_user(username, email, password)

    return {"username": username, "password": password}


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def login_user(client, user_data):
    url = reverse("web:token_obtain_pair")
    response = client.post(url, user_data, format="json")
    token = response.data["access"]
    yield token


class TestDistanceMeasurement:
    def test_unauthorized_api_user_list(self, client):
        url = reverse("sit_ble_devices:measurement-list")
        response = client.get(url)
        assert 401 == response.status_code

    @pytest.mark.django_db
    def test_authorized_api_user_list(self, client, login_user):
        url = reverse("sit_ble_devices:measurement-list")
        response = client.get(
            url,
            {},
            HTTP_AUTHORIZATION="Bearer {}".format(login_user),
            format="json",
        )
        assert 200 == response.status_code

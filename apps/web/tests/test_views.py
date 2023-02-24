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


class TestJWTLoginApi:
    @pytest.mark.django_db
    def test_login_jwt(self, client, user_data):
        url = reverse("web:token_obtain_pair")
        response = client.post(url, user_data, format="json")

        assert 200 == response.status_code
        assert "access" in response.data

    @pytest.mark.django_db
    def test_login_worng_login_jwt(self, client, user_data):
        url = reverse("web:token_obtain_pair")
        data = user_data
        data["password"] = "test"
        response = client.post(url, data, format="json")

        assert 401 == response.status_code


class TestUserApi:
    @pytest.fixture
    def login_user(self, client, user_data):
        url = reverse("web:token_obtain_pair")
        response = client.post(url, user_data, format="json")
        token = response.data["access"]
        yield token

    def test_unauthorized_api_user_list(self, client):
        url = reverse("web:user-list")
        response = client.get(url)
        assert 401 == response.status_code

    @pytest.mark.django_db
    def test_authorized_api_user_list(self, client, login_user):
        url = reverse("web:user-list")
        response = client.get(
            url,
            {},
            HTTP_AUTHORIZATION="Bearer {}".format(login_user),
            format="json",
        )
        assert 200 == response.status_code


def test_api_root(client):
    url = reverse("web:api-root")
    response = client.get(url)
    assert 200 == response.status_code

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from sit_ble_devices.models import (
    DistanceMeasurement,
    MeasurementTest,
    MeasurementTestSettings,
)
from sit_ble_devices.store.store import Store


# Create User
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


# For Store Tests
def store_cleanup():
    json_store = Store()
    connection_list = []
    json_store.set_value("websocket_connection", connection_list)
    json_store.set_value("device_list", connection_list)
    json_store.save()


@pytest.fixture()
def clean_store_files():
    # Code that will run before your test, for example:
    store_cleanup()
    # A test function will be run at this point
    yield
    # Code that will run after your test, for example:
    store_cleanup()


# Measurement Tests
@pytest.fixture()
@pytest.mark.django_db
def measurement_test_settings(user_data):
    user = User.objects.get(username=user_data["username"])
    test_settings = MeasurementTestSettings.objects.create(
        owner=user, test_name="Test", test_type="Static Test"
    )
    yield test_settings


@pytest.fixture()
@pytest.mark.django_db
def measurement_test(user_data, measurement_test_settings):
    user = User.objects.get(username=user_data["username"])
    measurement_test = MeasurementTest.objects.create(
        owner=user, test_settings=measurement_test_settings
    )
    yield measurement_test

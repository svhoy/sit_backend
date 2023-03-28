# Third Party
import pytest
from django.urls import reverse


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


class TestMeasurementTestSettings:
    @pytest.mark.django_db
    def test_test_settings_api_user_list(
        self, client, login_user, measurement_test_settings
    ):
        url = reverse("sit_ble_devices:test-settings-list")
        response = client.get(
            url,
            {},
            HTTP_AUTHORIZATION="Bearer {}".format(login_user),
            format="json",
        )
        assert 200 == response.status_code


class TestMeasurementTest:
    @pytest.mark.django_db
    def test_test_api_user_list(self, client, login_user, measurement_test):
        url = reverse("sit_ble_devices:test-list")
        response = client.get(
            url,
            {},
            HTTP_AUTHORIZATION="Bearer {}".format(login_user),
            format="json",
        )
        assert 200 == response.status_code

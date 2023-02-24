# Third Party
import pytest

from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_unauthorized_settings_request():
    api_client = APIClient()
    url = reverse("sit_settings:uwbdevicesettings-list")
    response = api_client.get(url)
    assert response.status_code == 401

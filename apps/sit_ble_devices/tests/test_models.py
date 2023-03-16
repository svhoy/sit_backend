import pytest
from sit_ble_devices.models import DistanceMeasurement


@pytest.mark.django_db
class TestDistanceModel:
    def test_create_distanceMeasurement(self):
        distance = DistanceMeasurement.objects.create(distance=1.1)
        assert distance.distance == 1.1

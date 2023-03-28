import pytest
from sit_ble_devices.models import (
    DistanceMeasurement,
    MeasurementTest,
    MeasurementTestSettings,
)


@pytest.mark.django_db
class TestDistanceModel:
    def test_create_distanceMeasurement(self):
        distance = DistanceMeasurement.objects.create(distance=1.1)
        assert distance.distance == 1.1

    def test_create_distanceMeasurementWithTest(self, measurement_test):
        distance = DistanceMeasurement.objects.create(
            distance=1.1, test=measurement_test
        )
        assert distance.distance == 1.1
        assert distance.test == measurement_test


@pytest.mark.django_db
class TestDistanceTestSettingsModel:
    def test_create_testSettings(self, measurement_test_settings):
        test_settings = MeasurementTestSettings.objects.get(pk=1)
        assert test_settings == measurement_test_settings

    def test_create_testSettings_min_measurements(
        self, measurement_test_settings
    ):
        test_settings = MeasurementTestSettings.objects.get(pk=1)
        test_settings.test_min_measurements = 50
        test_settings.save()
        assert test_settings.test_min_measurements == 50

    def test_create_testSettings_max_measurements(
        self, measurement_test_settings
    ):
        test_settings = MeasurementTestSettings.objects.get(pk=1)
        test_settings.test_max_measurements = 50
        test_settings.save()
        assert test_settings.test_max_measurements == 50


@pytest.mark.django_db
class TestDistanceTestModel:
    def test_create_testSettings(self, measurement_test):
        measurement_test_model = MeasurementTest.objects.get(pk=1)
        assert measurement_test_model == measurement_test

import pytest

from sit_ble_devices.models import (
    DistanceMeasurement,
    DeviceTests,
    DeviceTestGroups,
    UwbDevice,
)


@pytest.mark.django_db
class TestDistanceMeasurementModel:
    def test_create_distanceMeasurement(self):
        distance = DistanceMeasurement.objects.create(distance=1.1)
        assert DistanceMeasurement.objects.count() == 1
        assert DistanceMeasurement.objects.all()[0] == distance

    def test_create_distanceMeasurementWithTest(self, device_test):
        distance = DistanceMeasurement.objects.create(
            distance=1.1, test=device_test
        )

        assert DistanceMeasurement.objects.count() == 1
        assert DistanceMeasurement.objects.all()[0] == distance


@pytest.mark.django_db
class DeviceTestGroupsModel:
    def test_create_testGroup(self, device_test_group):
        test_group = DeviceTestGroups.objects.get(pk=1)
        assert test_group == device_test_group

    def test_create_testGroup_min_measurements(self, device_test_group):
        test_group = DeviceTestGroups.objects.get(pk=1)
        test_group.test_min_measurements = 50
        test_group.save()
        assert test_group.test_min_measurements == 50

    def test_create_testGroup_max_measurements(
        self, measurement_test_settings
    ):
        test_settings = DeviceTestGroups.objects.get(pk=1)
        test_settings.test_max_measurements = 50
        test_settings.save()
        assert test_settings.test_max_measurements == 50


@pytest.mark.django_db
class TestDeviceTestsModel:
    def test_create_deviceTest(self, device_test):
        device_test_model = DeviceTests.objects.get(pk=1)
        assert device_test_model == device_test


@pytest.mark.django_db
class DeviceTest:
    def test_create_Device(self, uwb_device_test):
        uwb_device_model = UwbDevice.objects.get(pk=1)
        assert uwb_device_model.device_name == "Test Device"
        assert uwb_device_model.device_id == "ABCDEF12345"

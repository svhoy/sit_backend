# Third Party
from django.test import TestCase

from ..models import UwbDeviceSettings


class UwbDeviceSettingsTest(TestCase):
    """Module for testing UWB Device Settings model"""

    # def setUp(self) -> None:
    #     UwbDeviceSettings.objects.create(name="TestSitSettingsTest")

    # def test_uwbsettings(self) -> None:
    #     test = UwbDeviceSettings.objects.get(name="TestSitSettingsTest")
    #     assert "TestSitSettingsTest" == test.name

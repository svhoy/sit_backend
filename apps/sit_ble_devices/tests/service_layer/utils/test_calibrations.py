import numpy as np
import numpy.testing as npt
import pytest
from sit_ble_devices.service_layer.utils.calibration.utils import (
    convert_distance_to_tof,
    convert_list_to_matrix,
)


@pytest.mark.asyncio
class TestCalibrationUitls:
    async def test_convert_distance_to_tof(
        self,
    ):
        distance = 7.914
        tof = await convert_distance_to_tof(distance)
        assert tof == 7.914 / 299702547

    async def test_convert_list_to_matrix(
        self, define_device_list, define_measurement_list, define_edm_measured
    ):
        matrix = await convert_list_to_matrix(
            define_device_list, define_measurement_list
        )
        npt.assert_array_equal(
            matrix,
            define_edm_measured,
        )

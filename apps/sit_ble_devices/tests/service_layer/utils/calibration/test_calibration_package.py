import numpy as np
import numpy.testing as npt
import pytest
from sit_ble_devices.service_layer.utils import calibration


@pytest.mark.asyncio
class TestCalibration:
    async def test_generic_calibration(
        self,
        define_device_list,
        define_edm_real_tof,
        define_edm_measured_tof,
        define_delay_array,
    ):
        pso = calibration.DecaCalibration(
            device_list=define_device_list,
            edm_measured=define_edm_measured_tof,
            edm_real=define_edm_real_tof,
        )
        delays = await pso.start_calibration_calc()
        npt.assert_allclose(define_delay_array, delays, atol=1e-9)

    async def test_pso_calibration(
        self,
        define_device_list,
        define_edm_real_tof,
        define_edm_measured_tof,
        define_delay_array,
    ):
        pso = calibration.PsoCalibration(
            device_list=define_device_list,
            edm_measured=define_edm_measured_tof,
            edm_real=define_edm_real_tof,
        )
        delays = await pso.start_calibration_calc()
        npt.assert_allclose(define_delay_array, delays, atol=1e-9)

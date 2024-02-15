import numpy as np
from sit_ble_devices.domain.model import calibration
from sit_ble_devices.service_layer.utils.Calibration.calibration import (
    CalibrationBase,
)


class PsoCalibration(CalibrationBase):
    def __init__(self, calibration_dom: calibration.Calibrations):
        self.iterations = 100
        self.avg_distance = []
        self.real_distance = []
        self.edm_measured = np.matrix([])
        self.edm_real = np.matrix([])
        self.events = []
        self.inital_delay = 513e-9
        self.perturbation_limit = 0.2e-9
        self.num_candidates = 1000
        super().__init__(calibration_dom)

    async def calibration_calc(self):
        raise NotImplementedError

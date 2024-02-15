import numpy as np
from sit_ble_devices.domain.model import calibration
from sit_ble_devices.models.devices import CalibrationsDistances
from sit_ble_devices.models.distances import DistanceMeasurement


class CalibrationBase:
    def __init__(self, calibration_dom: calibration.Calibrations):
        self.calibration = calibration_dom
        self.iterations = 100

    async def calibration_calc(self):
        raise NotImplementedError

    async def calc_delays(self, candidates):
        result = []
        for idx, device_id in enumerate(self.calibration.devices):
            tx_ant_dly = candidates[idx] * 0.44  # APS014 TX is 44%
            rx_ant_dly = candidates[idx] * 0.56  # APS014 RX is 56%
            result.append([device_id, tx_ant_dly, rx_ant_dly])
        return result

    async def get_distances(
        self, calibration_id, initiator, responder
    ) -> np.ndarray:
        results = await DistanceMeasurement.objects.filter(
            calibration__id=calibration_id,
            initiator__device_id=initiator,
            responder__device_id=responder,
        ).afirst()
        distances = np.array(results.values_list("distance"))
        return distances

    async def get_real_distance(
        self, calibration_id, initiator, responder
    ) -> np.ndarray:
        results = await CalibrationsDistances.objects.filter(
            calibration__id=calibration_id,
            initiator__device_id=initiator,
            responder__device_id=responder,
        ).afirst()
        distances = np.array(results.values_list("distance"))
        return distances

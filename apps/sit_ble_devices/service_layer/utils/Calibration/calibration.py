import numpy as np


class CalibrationBase:
    def __init__(self, device_list, *args, **kwargs):
        self.device_list = device_list
        self.edm_measured: np.ndarray = kwargs.get(
            "edm_measured", np.ndarray([])
        )
        self.edm_real: np.ndarray = kwargs.get("edm_real", np.ndarray([]))

    async def start_calibration_calc(self):
        raise NotImplementedError

    async def calc_delays(self, candidates):
        result = []
        for idx, device_id in enumerate(self.device_list):
            tx_ant_dly = candidates[idx] * 0.44  # APS014 TX is 44%
            rx_ant_dly = candidates[idx] * 0.56  # APS014 RX is 56%
            result.append([device_id, tx_ant_dly, rx_ant_dly])
        return result

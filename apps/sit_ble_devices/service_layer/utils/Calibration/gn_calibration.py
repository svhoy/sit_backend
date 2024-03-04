# pylint: disable=duplicate-code
import logging

import numpy as np

from ._base_calibration import CalibrationBase

# create logger
logger = logging.getLogger("service_layer.calibration.classes")


class GnCalibration(CalibrationBase):

    async def start_calibration_calc(self):
        cost = 0
        delays = np.array([])
        if self.edm_measured.size != 0:
            # TODO: Add GN optimization for EDM
            pass  # pylint: disable=unnecessary-pass
        elif (
            len(self.time_dict) >= 2
        ):  # Provide a minimum of 2 device measurements pairs
            # mixed_delays = np.array([])
            # delays = np.array([])
            # for measurement in self.time_dict:
            # TODO: Add GN optimization for TWR
            # mixed_delays = np.append(delays, delay)
            pass  # pylint: disable=unnecessary-pass
        # delays = self.calculated_lst_device_delays(mixed_delays)
        else:
            raise ValueError(
                "No EDM or Time List provied to calibrate antenna delays."
            )
        logger.info(f"Cost: {cost}, Delay: {delays}")
        return delays

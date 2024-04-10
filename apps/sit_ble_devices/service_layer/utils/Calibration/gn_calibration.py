# pylint: disable=duplicate-code
import logging

import numpy as np

from ..optimizer.gauss_newton import GaussNewtonOptimizer
from ._base_calibration import CalibrationBase

# create logger
logger = logging.getLogger("service_layer.calibration.classes")


class GaussNewtonCalibration(CalibrationBase):

    async def start_calibration_calc(self):
        delays = np.array([])
        if (
            len(self.measurement_pairs) >= 2
        ):  # Provide a minimum of 2 device measurements pairs
            mixed_delays = np.array([])
            for measurement in self.measurement_pairs:
                optimizer = GaussNewtonOptimizer()
                delay = optimizer.optimize(
                    self.objective_gauss_newton_function,
                    self.df_gauss_newton_function,
                    np.array([515e-9]),
                    max_iterations=self.iterations,
                    method="lm",
                    measurement=measurement,
                )
                mixed_delays = np.append(mixed_delays, delay)
                logger.info(f"Delay: {delay}")
            delays = await self.calculated_lst_device_delays(mixed_delays)
        else:
            raise ValueError(
                "No EDM or Time List provied to calibrate antenna delays."
            )
        logger.info(f"Delay: {delays}")
        return delays

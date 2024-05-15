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
                if self.measurement_type == "adstwr":
                    delay = optimizer.optimize(
                        fit_function=self.objective_gauss_newton_ads_function,
                        df_function=self.df_gauss_newton_ads_function,
                        initial_guess=np.array([1000e-9]),
                        max_iterations=self.iterations,
                        method="lm",
                        measurement=measurement,
                    )
                elif self.measurement_type == "sdstwr":
                    delay = optimizer.optimize(
                        fit_function=self.objective_gauss_newton_sds_function,
                        initial_guess=np.array([1000e-9]),
                        max_iterations=self.iterations,
                        method="lm",
                        measurement=measurement,
                    )
                elif self.measurement_type == "sstwr":
                    delay = optimizer.optimize(
                        fit_function=self.objective_gauss_newton_sstwr_function,
                        initial_guess=np.array([1000e-9]),
                        max_iterations=self.iterations,
                        method="lm",
                        measurement=measurement,
                    )
                else:
                    raise ValueError("Invalid measurement type provided.")
                mixed_delays = np.append(mixed_delays, delay)
                logger.info(f"Delay: {delay}")
            delays = await self.calculated_lst_device_delays(mixed_delays)
            logger.debug(f"Delays: {delays}")
        else:
            raise ValueError(
                "No EDM or Time List provied to calibrate antenna delays."
            )
        logger.info(f"Delay: {delays}")
        return delays

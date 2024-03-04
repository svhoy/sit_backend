import logging

import numpy as np
import pyswarms as ps

from ._base_calibration import CalibrationBase

# create logger
logger = logging.getLogger("service_layer.calibration.classes")


class PsoCalibration(CalibrationBase):
    async def start_calibration_calc(self):
        options = {
            "c1": 0.5,
            "c2": 0.3,
            "w": 0.3,
        }
        cost = 0
        delays = np.array([])
        if self.edm_measured.size != 0:
            optimizer = ps.single.GlobalBestPSO(
                n_particles=self.n_particles,
                dimensions=len(self.device_list),
                options=options,
                bounds=self.bounds,
            )
            cost, delays = optimizer.optimize(
                self.objective_edm_function, iters=self.iterations
            )
        elif (
            len(self.time_dict) >= 2
        ):  # Provide a minimum of 2 device measurements pairs
            mixed_delays = np.array([])
            delays = np.array([])
            for measurement in self.time_dict:
                optimizer = ps.single.GlobalBestPSO(
                    n_particles=self.n_particles,
                    dimensions=1,
                    options=options,
                    bounds=self.bounds,
                )
                cost, delay = optimizer.optimize(
                    self.objective_time_function,
                    iters=self.iterations,
                    measurement=measurement,
                )
                mixed_delays = np.append(delays, delay)

            delays = self.calculated_lst_device_delays(mixed_delays)
        else:
            raise ValueError(
                "No EDM or Times provied to calibrate antenna delays."
            )
        logger.info(f"Cost: {cost}, Delay: {delays}")
        return delays

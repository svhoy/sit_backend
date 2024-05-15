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
            if (
                self.measurement_type == "adstwr"
                or self.measurement_type == "sdstwr"
            ):
                cost, delays = optimizer.optimize(
                    self.objective_edm_dstwr_function, iters=self.iterations
                )
            elif self.measurement_type == "sstwr":
                cost, delays = optimizer.optimize(
                    self.objective_edm_sstwr_function, iters=self.iterations
                )
            else:
                raise ValueError("Invalid measurement type provided.")
        elif (
            len(self.measurement_pairs) >= 2
        ):  # Provide a minimum of 2 device measurements pairs
            mixed_delays = np.array([])
            delays = np.array([])
            for measurement in self.measurement_pairs:
                optimizer = ps.single.GlobalBestPSO(
                    n_particles=self.n_particles,
                    dimensions=1,
                    options=options,
                    bounds=self.bounds,
                )
                if self.measurement_type == "adstwr":
                    cost, delay = optimizer.optimize(
                        self.objective_pso_adstwr_function,
                        iters=self.iterations,
                        measurements=measurement,
                    )
                    mixed_delays = np.append(mixed_delays, delay[0])
                elif self.measurement_type == "sdstwr":
                    cost, delay = optimizer.optimize(
                        self.objective_pso_sdstwr_function,
                        iters=self.iterations,
                        measurements=measurement,
                    )
                    mixed_delays = np.append(mixed_delays, delay[0])
                elif self.measurement_type == "sstwr":
                    cost, delay = optimizer.optimize(
                        self.objective_pso_sstwr_function,
                        iters=self.iterations,
                        measurements=measurement,
                    )
                    mixed_delays = np.append(mixed_delays, delay[0])
                else:
                    raise ValueError("Invalid measurement type provided.")

            delays = await self.calculated_lst_device_delays(mixed_delays)
        else:
            raise ValueError(
                "No EDM or Measurements provied to calibrate antenna delays."
            )

        logger.info(f"Cost: {cost}, Delay: {delays}")
        return delays

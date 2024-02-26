import logging

import numpy as np
import pyswarms as ps

from .calibration import CalibrationBase

# create logger
logger = logging.getLogger("service_layer.calibration.classes")


class PsoCalibration(CalibrationBase):
    def __init__(self, device_list, *args, **kwargs):
        self.iterations = kwargs.get("iterations", 100)
        self.n_particles = kwargs.get("n_particles", 50)
        self.bounds = kwargs.get(
            "bounds", ([450e-9, 450e-9, 450e-9], [600e-9, 600e-9, 600e-9])
        )

        super().__init__(device_list, *args, **kwargs)

    async def start_calibration_calc(self):
        options = {"c1": 0.5, "c2": 0.3, "w": 0.3}

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
            logger.info(f"Cost: {cost}, Delay: {delays}")

        return delays

    def distance_func(self, delay_candidates: np.ndarray) -> float:
        row, column = self.edm_measured.shape
        edm_candidate = np.empty((row, column))
        for i in range(0, row):
            for j in range(0, column):
                if self.edm_measured[i, j] != 0:
                    edm_candidate[i, j] = (
                        (4 * self.edm_measured[i, j])
                        - (
                            (2 * delay_candidates[i])
                            + (2 * delay_candidates[j])
                        )
                    ) / 4.0
                else:
                    edm_candidate[i, j] = 0
        norm_diff = np.linalg.norm(self.edm_real - edm_candidate)
        return norm_diff

    def objective_edm_function(self, delay_candidates: np.ndarray):
        n_particales = delay_candidates.shape[0]
        dist = [
            self.distance_func(delay_candidates[i])
            for i in range(n_particales)
        ]
        return dist

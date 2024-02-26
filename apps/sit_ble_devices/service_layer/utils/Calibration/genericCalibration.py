import logging

import numpy as np

from .calibration import CalibrationBase

# create logger
logger = logging.getLogger("service_layer.calibration.classes")


class DecaCalibration(CalibrationBase):
    def __init__(self, device_list, *args, **kwargs):
        self.iterations = kwargs.get("iterations", 100)
        self.inital_delay = kwargs.get("inital_delay", 513e-9)
        self.perturbation_limit = kwargs.get("perturbation_limit", 0.2e-9)
        self.num_candidates = kwargs.get("num_candidates", 1000)
        super().__init__(device_list, *args, **kwargs)

    async def start_calibration_calc(self):
        candidates = np.zeros((self.num_candidates, 4))
        best_canidate = []
        for i in range(self.iterations):
            logger.debug("Running")
            candidates = await self.populate_candidates(i, candidates)
            candidates = await self.evaluate_candidates(candidates)

        best_canidate = candidates[0]
        return best_canidate[:3]

    async def populate_candidates(
        self, iteration: int, candidates: np.ndarray
    ) -> np.ndarray:
        if iteration == 0:
            for index in range(self.num_candidates):
                arr = self.inital_delay + np.random.uniform(
                    -6e-9,
                    6e-9,
                    3,
                )
                arr = np.append(arr, 0)
                candidates[index] = arr
        else:
            copied_elements = int(candidates.shape[0] / 4)
            best_25 = candidates[:copied_elements]
            randomized_arrays = []
            for _ in range(3):
                for candidate in best_25:
                    randomized_shifts = np.random.uniform(
                        -self.perturbation_limit,
                        self.perturbation_limit,
                        candidate.shape,
                    )
                    rnd_candidate = np.add(candidate, randomized_shifts)
                    randomized_arrays.append(rnd_candidate)

            candidates = np.concatenate([best_25, randomized_arrays])

        if iteration % 20 == 0 and iteration != 0:
            self.perturbation_limit = self.perturbation_limit / 2

        return candidates

    async def evaluate_candidates(self, candidates):
        row, column = self.edm_measured.shape
        edm_candidate = np.empty((row, column))
        for index, candidate in enumerate(candidates):
            for i in range(0, row):
                for j in range(0, column):
                    if self.edm_measured[i, j] != 0:
                        edm_candidate[i, j] = (
                            (4 * self.edm_measured[i, j])
                            - ((2 * candidate[i]) + (2 * candidate[j]))
                        ) / 4.0
                    else:
                        edm_candidate[i, j] = 0
                norm_diff = np.linalg.norm(self.edm_real - edm_candidate)
                candidates[index, 3] = norm_diff

        sorted_indices = np.argsort(candidates[:, 3])
        sorted_candidates = candidates[sorted_indices]
        logger.debug(f"Sorted Candidate: {sorted_candidates}")
        return sorted_candidates

    async def find_best_candidate(self, candidates: np.ndarray):
        return candidates[0]

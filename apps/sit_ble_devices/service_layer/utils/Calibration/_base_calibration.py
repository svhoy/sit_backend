# pylint: disable=duplicate-code
import time

import numpy as np

SPEED_OF_LIGHT = 299702547  # m/s

import logging

logger = logging.getLogger("sit_calibration.classes")


class CalibrationBase:
    def __init__(self, device_list, *args, **kwargs):
        self.device_list = device_list
        self.edm_measured: np.ndarray = kwargs.get(
            "edm_measured", np.array([])
        )
        self.edm_real: np.ndarray = kwargs.get("edm_real", np.array([]))
        self.measurement_pairs = kwargs.get("measurement_pairs", [])
        self.iterations = kwargs.get("iterations", 100)
        self.n_particles = kwargs.get("n_particles", 50)
        self.bounds = kwargs.get(
            "bounds", ([450e-9, 450e-9, 450e-9], [600e-9, 600e-9, 600e-9])
        )

    async def start_calibration_calc(self):
        raise NotImplementedError

    async def calc_tx_rx_delays(self, candidates:list[float]) -> list[list[str, float, float]]:
        result = []
        for idx, device_id in enumerate(self.device_list):
            tx_ant_dly = candidates[idx] * 0.44  # APS014 TX is 44%
            rx_ant_dly = candidates[idx] * 0.56  # APS014 RX is 56%
            result.append([device_id, tx_ant_dly, rx_ant_dly])
        return result

    async def calculated_lst_device_delays(
        self, mixed_delays: np.ndarray
    ) -> np.ndarray:
        transform_matrix = np.matrix([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
        inv_transform_matrix = np.linalg.inv(transform_matrix)
        transpose_mixed_delays = np.transpose(mixed_delays)
        delays = np.array([])
        if mixed_delays.size == 3:
            delays = inv_transform_matrix.dot(transpose_mixed_delays)
        elif mixed_delays.size > 3:
            transpose_transform_matrix = transform_matrix.transpose()

            mm = transpose_transform_matrix.dot(transform_matrix)
            inv_mm = np.linalg.inv(mm)
            mmm = inv_mm.dot(transpose_transform_matrix)

            delays = mmm.dot(mixed_delays)
            # Short way (TODO:Test)
            # delays = np.linalg.lstsq(
            #     transform_matrix, mixed_delays, rcond=None
            # )
        else:
            raise ValueError("Invalid delays list provided")
        return delays.tolist()[0]

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

    def objective_pso_function(
        self, delay_candidates: np.ndarray, measurements: dict
    ):
        time_diff = 0

        # Measurements should be a list of every measurement between these two devices.
        # In PSO we take the mean of all measurements and then calculate the estimated
        # Time of Flight before looking how good our candidates are.
        time_round_1 = measurements["time_round_1"].mean()
        time_round_2 = measurements["time_round_2"].mean()
        time_reply_1 = measurements["time_reply_1"].mean()
        time_reply_2 = measurements["time_reply_2"].mean()
        error_tof = (
            time_round_1 * time_round_2
            - time_reply_1 * time_reply_2
            - (
                time_reply_1 * delay_candidates[:, 0]
                + time_reply_2 * delay_candidates[:, 0]
                + 4 * (delay_candidates[:, 0] ** 2)
            )
        ) / (
            time_round_1
            + time_round_2
            + time_reply_1
            + time_reply_2
            + 2 * delay_candidates[:, 0]
        )
        error_distance = error_tof * SPEED_OF_LIGHT
        time_diff = abs(measurements["real_distance"] - error_distance)
        return time_diff

    def objective_gauss_newton_function(
        self,
        delay_candidate: np.array,
        time_round_1: float,
        time_round_2: float,
        time_reply_1: float,
        time_reply_2: float,
        real_tof: float,
    ) -> np.ndarray:
        time_diff = 0
        # Measurements should be a dict with the timestamps. The Timestamps are a list with
        # eache entry represent a single measurement timestamp.
        # For Gauss Newton we caclulate the estimated Time of Flight for every measurement
        # with the current candidate and then calculate the error.

        error_tof = (
            time_round_1 * time_round_2
            - time_reply_1 * time_reply_2
            - (
                time_reply_1 * delay_candidate[0]
                + time_reply_2 * delay_candidate[0]
                + 4 * (delay_candidate[0] ** 2)
            )
        ) / (
            time_round_1
            + time_round_2
            + time_reply_1
            + time_reply_2
            + 2 * delay_candidate[0]
        )
        time_diff = abs(real_tof - error_tof)

        return time_diff

    def df_gauss_newton_function(
        self,
        delay_candidate: np.array,
        time_round_1: float,
        time_round_2: float,
        time_reply_1: float,
        time_reply_2: float,
        real_tof: float,
    ) -> np.ndarray:

        error_tof = (
            -time_round_1
            * (
                2 * time_round_2
                + time_reply_1
                + time_reply_2
                + 8 * delay_candidate[0]
            )
            - time_round_2
            * (time_reply_1 + time_reply_2 + 8 * delay_candidate[0])
            - 8 * delay_candidate[0] * (time_reply_1 + time_reply_2)
            - 8 * delay_candidate[0] ** 2
            - time_reply_1**2
            - time_reply_2**2
        ) / (
            (
                time_round_1
                + time_round_2
                + time_reply_1
                + time_reply_2
                + 2 * delay_candidate[0]
            )
            ** 2
        )

        return np.array([error_tof]).reshape(-1, 1)

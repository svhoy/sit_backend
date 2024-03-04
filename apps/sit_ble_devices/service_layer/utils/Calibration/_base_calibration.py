# pylint: disable=duplicate-code
import numpy as np

SPEED_OF_LIGHT = 299702547  # m/s


class CalibrationBase:
    def __init__(self, device_list, *args, **kwargs):
        self.device_list = device_list
        self.edm_measured: np.ndarray = kwargs.get(
            "edm_measured", np.ndarray([])
        )
        self.edm_real: np.ndarray = kwargs.get("edm_real", np.ndarray([]))
        self.time_dict = kwargs.get("time_list", np.ndarray([]))
        self.iterations = kwargs.get("iterations", 100)
        self.n_particles = kwargs.get("n_particles", 50)
        self.bounds = kwargs.get(
            "bounds", ([450e-9, 450e-9, 450e-9], [600e-9, 600e-9, 600e-9])
        )

    async def start_calibration_calc(self):
        raise NotImplementedError

    async def calc_tx_rx_delays(self, candidates):
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

    def objective_time_function(
        self, delay_candidates: np.ndarray, measurement: dict
    ):
        time_diff = 0
        time_round_1 = measurement["time_round_1"]
        time_round_2 = measurement["time_round_2"]
        time_reply_1 = measurement["time_reply_1"]
        time_reply_2 = measurement["time_reply_2"]
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
        time_diff = abs(measurement["real_distance"] - error_distance)
        return time_diff

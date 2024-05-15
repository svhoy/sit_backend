import numpy as np


class SimpleCalibrationBase:
    def __init__(self, measurement_list, device_list):
        self.measurement_list = measurement_list
        self.device_list = device_list

    async def calc_tx_rx_delays(
        self, candidates: list[float]
    ) -> list[list[str, float, float]]:
        result = []
        for idx, device_id in enumerate(self.device_list):
            tx_ant_dly = candidates[idx] * 0.44  # APS014 TX is 44%
            rx_ant_dly = candidates[idx] * 0.56  # APS014 RX is 56%
            result.append([device_id, tx_ant_dly, rx_ant_dly])
        return result

    async def start_calibration_calc(self):
        raise NotImplementedError


class SimpleCalibration(SimpleCalibrationBase):
    def __init__(self, measurement_list):
        device_list = [
            measurement_list[0]["devices"][0],
            measurement_list[0]["devices"][1],
            measurement_list[0]["devices"][2],
        ]
        super().__init__(measurement_list, device_list)

    async def start_calibration_calc(self):
        results = []
        for measurement in self.measurement_list:
            ant_delay = (
                np.mean(measurement["time_c_i"])
                - np.mean(measurement["time_b_i"])
                + measurement["real_tof_a_c"]
                - measurement["real_tof_a_b"]
                - measurement["real_tof_b_c"]
            )
            results.append(ant_delay)
        results_reodered = [results[2], results[0], results[1]]
        return results_reodered


class ExtendedCalibration(SimpleCalibrationBase):
    def __init__(self, measurement_list):
        device_list = [
            measurement_list[0]["devices"][0],
            measurement_list[0]["devices"][1],
            measurement_list[0]["devices"][2],
        ]
        super().__init__(measurement_list, device_list)

    async def start_calibration_calc(self):
        results = []
        for measurement in self.measurement_list:
            ant_delay = (
                (
                    (
                        np.mean(measurement["time_c_i"])
                        - np.mean(measurement["time_c_ii"])
                    )
                    / 2
                )
                - (
                    (
                        np.mean(measurement["time_b_i"])
                        - np.mean(measurement["time_b_ii"])
                    )
                    / 2
                )
                + measurement["real_tof_a_c"]
                - measurement["real_tof_a_b"]
                - measurement["real_tof_b_c"]
            )
            results.append(ant_delay)
        # Results are reordered to match the order of the devices
        results_reodered = [results[2], results[0], results[1]]
        return results_reodered


class TwoDeviceCalibration(SimpleCalibrationBase):

    async def start_calibration_calc(self):
        time_m21 = np.mean(
            self.measurement_list[0]["time_m21"],
            where=self.measurement_list[0]["time_m21"] > 0,
        )
        time_m31 = np.mean(
            self.measurement_list[0]["time_m31"],
            where=self.measurement_list[0]["time_m31"] > 0,
        )
        time_a21 = np.mean(
            self.measurement_list[0]["time_a21"],
            where=self.measurement_list[0]["time_a21"] > 0,
        )
        time_a31 = np.mean(
            self.measurement_list[0]["time_a31"],
            where=self.measurement_list[0]["time_a31"] > 0,
        )
        time_b21 = np.mean(
            self.measurement_list[0]["time_b21"],
            where=self.measurement_list[0]["time_b21"] > 0,
        )
        time_b31 = np.mean(
            self.measurement_list[0]["time_b31"],
            where=self.measurement_list[0]["time_b31"] > 0,
        )
        ant_delay_a = (
            time_m21
            - (time_b21 * (time_m31 / time_b31))
            + self.measurement_list[0]["real_tof_b_c"]
            - self.measurement_list[0]["real_tof_a_b"]
            - self.measurement_list[0]["real_tof_a_c"]
        )

        ant_delay_b = (
            (time_b21 * (time_m31 / time_b31))
            - (time_a21 * (time_m31 / time_a31))
            - self.measurement_list[0]["real_tof_b_c"]
            - self.measurement_list[0]["real_tof_a_b"]
            + self.measurement_list[0]["real_tof_a_c"]
        )

        time_m31 = np.mean(
            self.measurement_list[1]["time_m31"],
            where=self.measurement_list[1]["time_m31"] > 0,
        )
        time_a21 = np.mean(
            self.measurement_list[1]["time_a21"],
            where=self.measurement_list[1]["time_a21"] > 0,
        )
        time_a31 = np.mean(
            self.measurement_list[1]["time_a31"],
            where=self.measurement_list[1]["time_a31"] > 0,
        )
        time_b21 = np.mean(
            self.measurement_list[1]["time_b21"],
            where=self.measurement_list[1]["time_b21"] > 0,
        )
        time_b31 = np.mean(
            self.measurement_list[1]["time_b31"],
            where=self.measurement_list[1]["time_b31"] > 0,
        )
        ant_delay_c = (
            (time_b21 * (time_m31 / time_b31))
            - (time_a21 * (time_m31 / time_a31))
            - self.measurement_list[1]["real_tof_b_c"]
            - self.measurement_list[1]["real_tof_a_b"]
            + self.measurement_list[1]["real_tof_a_c"]
        )

        return [ant_delay_a, ant_delay_b, ant_delay_c]

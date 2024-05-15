import logging
from typing import Tuple

import numpy as np
from sit_ble_devices.domain.model.distances import (
    CalibrationMeasurements,
    DistanceMeasurement,
)
from sit_ble_devices.service_layer.utils import calibration

logger = logging.getLogger("domain.model.calibration")


class CalibrationDistance:
    def __init__(
        self,
        calibration_id,
        initiator_id,
        responder_id,
        distance,
        *args,
        **kwargs,
    ):
        self.distance_id = kwargs.get("distance_id", None)
        self.calibration_id = calibration_id
        self.initiator_id = initiator_id
        self.responder_id = responder_id
        self.distance = distance
        self.measurements = []


class Calibrations:
    def __init__(
        self,
        devices,
        **kwargs,
    ):
        self.calibration_id: int = kwargs.get("calibration_id", None)
        self.calibration_type: str = kwargs.get("calibration_type", None)
        self.measurement_type: str = kwargs.get("measurement_type", None)
        self.devices: list[str] = devices
        self.temperature = kwargs.get("temperature", None)
        self.cali_distances: list[CalibrationDistance] = []
        self.distances: list[DistanceMeasurement] = []
        self.measurments: list[CalibrationMeasurements] = []
        self.events = []

    async def append_cali_distances(
        self, cali_distance_dom: CalibrationDistance
    ):
        self.cali_distances.append(cali_distance_dom)

    def append_distances(self, distances: DistanceMeasurement):
        self.distances = distances

    def append_measurements(self, measurements: CalibrationMeasurements):
        self.measurments = measurements

    async def start_calibration_calc(self) -> list[float]:
        calibration_instance = None
        match self.calibration_type:
            case "Antenna Calibration (ASP014) - SSTWR":
                edm_measured, edm_real = await self.setup_edms()
                calibration_instance = calibration.DecaCalibration(
                    device_list=self.devices,
                    edm_measured=edm_measured,
                    edm_real=edm_real,
                    measurement_type="sstwr",
                )
            case "Antenna Calibration (ASP014) - DSTWR":
                edm_measured, edm_real = await self.setup_edms()
                calibration_instance = calibration.DecaCalibration(
                    device_list=self.devices,
                    edm_measured=edm_measured,
                    edm_real=edm_real,
                    measurement_type="adstwr",
                )
            case "Antenna Calibration (PSO) - EDM SSTWR":
                edm_measured, edm_real = await self.setup_edms()
                calibration_instance = calibration.PsoCalibration(
                    device_list=self.devices,
                    edm_measured=edm_measured,
                    edm_real=edm_real,
                    measurement_type="sstwr",
                )
            case "Antenna Calibration (PSO) - EDM DSTWR":
                edm_measured, edm_real = await self.setup_edms()
                calibration_instance = calibration.PsoCalibration(
                    device_list=self.devices,
                    edm_measured=edm_measured,
                    edm_real=edm_real,
                    measurement_type="adstwr",
                )
            case "Antenna Calibration (PSO) - SSTWR":
                measurement_list = await self.get_measurement_list()
                calibration_instance = calibration.PsoCalibration(
                    device_list=self.devices,
                    measurement_pairs=measurement_list,
                    measurement_type="sstwr",
                    bounds=([500e-9], [1200e-9]),
                )
            case "Antenna Calibration (PSO) - SDS":
                measurement_list = await self.get_measurement_list()
                calibration_instance = calibration.PsoCalibration(
                    device_list=self.devices,
                    measurement_pairs=measurement_list,
                    measurement_type="sdstwr",
                    bounds=([500e-9], [1200e-9]),
                )
            case "Antenna Calibration (PSO) - ADS":
                measurement_list = await self.get_measurement_list()
                calibration_instance = calibration.PsoCalibration(
                    device_list=self.devices,
                    measurement_pairs=measurement_list,
                    measurement_type="adstwr",
                    bounds=([500e-9], [1200e-9]),
                )
            case "Antenna Calibration (GNA) - SSTWR":
                measurement_list = await self.get_measurement_list()
                calibration_instance = calibration.GaussNewtonCalibration(
                    device_list=self.devices,
                    measurement_pairs=measurement_list,
                    measurement_type="sstwr",
                )
            case "Antenna Calibration (GNA) - SDS":
                measurement_list = await self.get_measurement_list()
                calibration_instance = calibration.GaussNewtonCalibration(
                    device_list=self.devices,
                    measurement_pairs=measurement_list,
                    measurement_type="sdstwr",
                )
            case "Antenna Calibration (GNA) - ADS":
                measurement_list = await self.get_measurement_list()
                calibration_instance = calibration.GaussNewtonCalibration(
                    device_list=self.devices,
                    measurement_pairs=measurement_list,
                    measurement_type="adstwr",
                )
            case "Antenna Calibration (Simple)":
                measurement_list = (
                    await self.get_calibration_measurement_list()
                )
                calibration_instance = calibration.SimpleCalibration(
                    measurement_list=measurement_list,
                )

            case "Antenna Calibration (Extended)":
                measurement_list = (
                    await self.get_calibration_measurement_list()
                )
                calibration_instance = calibration.ExtendedCalibration(
                    measurement_list=measurement_list,
                )
            case "Antenna Calibration (Two Device)":
                measurement_list = (
                    await self.get_calibration_measurement_list()
                )
                calibration_instance = calibration.TwoDeviceCalibration(
                    measurement_list=measurement_list,
                    device_list=self.devices,
                )
            case _:
                raise ValueError(
                    f"Invalid calibration type: {self.calibration_type}"
                )

        if calibration_instance is not None:
            result = await calibration_instance.start_calibration_calc()
            result = await calibration_instance.calc_tx_rx_delays(result)
            logger.info(f"Calc Results: {result}")
        else:
            result = -1
        return result

    async def setup_edms(self) -> Tuple[np.ndarray, np.ndarray]:
        avg_distances = []
        real_distances = []
        edm_measured = np.array([])
        edm_real = np.array([])

        for initiator in self.devices:
            for responder in self.devices:
                if responder != initiator:
                    distances = await self.filter_distances(
                        initiator, responder
                    )
                    avg_distance = np.mean(distances)
                    avg_distance = (
                        await calibration.utils.convert_distance_to_tof(
                            avg_distance
                        )
                    )
                    avg_distances.append(avg_distance)

                    real_distance = await self.filter_real_distances(
                        initiator, responder
                    )
                    real_distance = (
                        await calibration.utils.convert_distance_to_tof(
                            real_distance
                        )
                    )
                    real_distances.append(real_distance)
                else:
                    avg_distances.append(0)
                    real_distances.append(0)

        edm_measured = await calibration.utils.convert_list_to_matrix(
            self.devices, avg_distances
        )
        edm_real = await calibration.utils.convert_list_to_matrix(
            self.devices, real_distances
        )

        return edm_measured, edm_real

    async def filter_distances(self, initiator, responder) -> np.ndarray:
        filtered_distances = np.array(
            [
                distance.distance
                for distance in self.measurments
                if distance.device_a == initiator
                and distance.device_b == responder
            ]
        )
        return filtered_distances

    async def filter_real_distances(self, initiator, responder) -> np.ndarray:
        for distance in self.cali_distances:
            if (
                distance.initiator_id == initiator
                and distance.responder_id == responder
            ):
                return distance.distance

        raise ValueError(f"Distance not found for {initiator} and {responder}")

    async def filter_times(self, initiator, responder) -> dict:
        # TODO: Filter for times instaned of distances and pack in a good workable format
        measurement_dict = {
            "initator": initiator,
            "responder": responder,
            "time_round_1": np.array([]),
            "time_round_2": np.array([]),
            "time_reply_1": np.array([]),
            "time_reply_2": np.array([]),
        }
        for measurement in self.measurments:
            if (
                measurement.device_a == initiator
                and measurement.device_b == responder
            ):
                measurement_dict["time_round_1"] = np.append(
                    measurement_dict["time_round_1"],
                    measurement.time_round_1,
                )
                measurement_dict["time_round_2"] = np.append(
                    measurement_dict["time_round_2"],
                    measurement.time_round_2,
                )
                measurement_dict["time_reply_1"] = np.append(
                    measurement_dict["time_reply_1"],
                    measurement.time_reply_1,
                )
                measurement_dict["time_reply_2"] = np.append(
                    measurement_dict["time_reply_2"],
                    measurement.time_reply_2,
                )

        measurement_dict["real_distance"] = await self.filter_real_distances(
            initiator, responder
        )
        measurement_dict["real_tof"] = (
            await calibration.utils.convert_distance_to_tof(
                measurement_dict["real_distance"]
            )
        )
        return measurement_dict

    async def get_measurement_list(self) -> list[float]:
        measurement_list = []
        for idx, initiator in enumerate(self.devices):
            for responder in self.devices[idx + 1 :]:
                measurement_dict = await self.filter_times(
                    initiator, responder
                )
                measurement_list.append(measurement_dict)

        return measurement_list

    async def filter_two_device_times(self, devices: list[str]) -> dict:
        # TODO: Filter for times instaned of distances and pack in a good workable format
        measurement_dict = {
            "devices": devices,
            "time_m21": np.array([]),
            "time_m31": np.array([]),
            "time_a21": np.array([]),
            "time_a31": np.array([]),
            "time_b21": np.array([]),
            "time_b31": np.array([]),
            "time_b_i": np.array([]),
            "time_b_ii": np.array([]),
            "time_c_i": np.array([]),
            "time_c_ii": np.array([]),
        }
        for measurement in self.measurments:
            if (
                measurement.device_a == devices[0]
                and measurement.device_b == devices[1]
                and measurement.device_c == devices[2]
            ):
                measurement_dict["time_m21"] = np.append(
                    measurement_dict["time_m21"],
                    measurement.time_m21,
                )
                measurement_dict["time_m31"] = np.append(
                    measurement_dict["time_m31"],
                    measurement.time_m31,
                )
                measurement_dict["time_a21"] = np.append(
                    measurement_dict["time_a21"],
                    measurement.time_a21,
                )
                measurement_dict["time_a31"] = np.append(
                    measurement_dict["time_a31"],
                    measurement.time_a31,
                )
                measurement_dict["time_b21"] = np.append(
                    measurement_dict["time_b21"],
                    measurement.time_b21,
                )
                measurement_dict["time_b31"] = np.append(
                    measurement_dict["time_b31"],
                    measurement.time_b31,
                )
                measurement_dict["time_b_i"] = np.append(
                    measurement_dict["time_b_i"],
                    measurement.time_b_i,
                )
                measurement_dict["time_b_ii"] = np.append(
                    measurement_dict["time_b_ii"],
                    measurement.time_b_ii,
                )
                measurement_dict["time_c_i"] = np.append(
                    measurement_dict["time_c_i"],
                    measurement.time_c_i,
                )
                measurement_dict["time_c_ii"] = np.append(
                    measurement_dict["time_c_ii"],
                    measurement.time_c_ii,
                )

        measurement_dict["real_tof_a_b"] = (
            await calibration.utils.convert_distance_to_tof(
                await self.filter_real_distances(devices[0], devices[1])
            )
        )
        measurement_dict["real_tof_a_c"] = (
            await calibration.utils.convert_distance_to_tof(
                await self.filter_real_distances(devices[0], devices[2])
            )
        )
        measurement_dict["real_tof_b_c"] = (
            await calibration.utils.convert_distance_to_tof(
                await self.filter_real_distances(devices[1], devices[2])
            )
        )
        return measurement_dict

    async def get_calibration_measurement_list(self):
        devices = self.devices
        measurement_list = []
        for _ in range(len(self.devices)):
            measurement_list.append(
                await self.filter_two_device_times(devices)
            )
            device = devices.pop(0)
            devices.append(device)

        return measurement_list

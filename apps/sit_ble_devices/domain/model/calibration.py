import logging
from typing import Tuple

import numpy as np
from sit_ble_devices.domain.model.distances import DistanceMeasurement
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
        self.events = []

    async def append_cali_distances(
        self, cali_distance_dom: CalibrationDistance
    ):
        self.cali_distances.append(cali_distance_dom)

    def append_distances(self, distances: DistanceMeasurement):
        self.distances = distances

    async def start_calibration_calc(self) -> list[float]:
        calibration_instance = None
        match self.calibration_type:
            case "Antenna Calibration (ASP014)":
                edm_measured, edm_real = await self.setup_edms()
                calibration_instance = calibration.DecaCalibration(
                    device_list=self.devices,
                    edm_measured=edm_measured,
                    edm_real=edm_real,
                )
            case "Antenna Calibration (PSO) - EDM":
                edm_measured, edm_real = await self.setup_edms()
                calibration_instance = calibration.PsoCalibration(
                    device_list=self.devices,
                    edm_measured=edm_measured,
                    edm_real=edm_real,
                )
            case "Antenna Calibration (PSO) - ADS":
                measurement_list = await self.get_measurement_list()
                calibration_instance = calibration.PsoCalibration(
                    device_list=self.devices,
                    measurement_pairs=measurement_list,
                    bounds=([500e-9], [1200e-9]),
                )
            case "Antenna Calibration (GNA) - ADS":
                measurement_list = await self.get_measurement_list()
                calibration_instance = calibration.GaussNewtonCalibration(
                    device_list=self.devices,
                    measurement_pairs=measurement_list,
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
                for distance in self.distances
                if distance.initiator_id == initiator
                and distance.responder_id == responder
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
        for measurement in self.distances:
            if (
                measurement.initiator_id == initiator
                and measurement.responder_id == responder
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

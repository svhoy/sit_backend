import logging
from typing import TYPE_CHECKING, Tuple

import numpy as np
from sit_ble_devices.domain.model.distances import DistanceMeasurement
from sit_ble_devices.service_layer.utils import calibration

if TYPE_CHECKING:
    from sit_ble_devices.domain.model.uwbdevice import UwbDevice

logger = logging.getLogger("domain.model.calibration")


class CalibrationDistance:
    def __init__(
        self,
        calibration_id,
        initiator_id,
        responder_id,
        distance,
        distance_id=None,
    ):
        self.distance_id = distance_id
        self.calibration_id = calibration_id
        self.initiator_id = initiator_id
        self.responder_id = responder_id
        self.distance = distance


class Calibrations:
    def __init__(
        self,
        devices,
        calibration_id=None,
        calibration_type=None,
        measurement_type=None,
    ):
        self.calibration_id: int = calibration_id
        self.calibration_type: str = calibration_type
        self.devices: list[str] = devices
        self.measurement_type: str = measurement_type
        self.cali_distances: list[CalibrationDistance]
        self.distances: list[DistanceMeasurement]
        self.events = []

    def append_cali_distances(self, cali_distance_dom: CalibrationDistance):
        self.cali_distances.append(cali_distance_dom)

    def append_distances(self, distances: DistanceMeasurement):
        self.distances = distances

    async def start_calibration_calc(self) -> list[float]:
        calibration_instance = None
        match self.calibration_type:
            case "Antenna Calibration (ASP014)":
                edm_measured, edm_real = self.setup_edms()
                calibration_instance = calibration.DecaCalibration(
                    device_list=self.devices,
                    edm_measured=edm_measured,
                    edm_real=edm_real,
                )
            case "Antenna Calibration (PSO) - EDM":
                edm_measured, edm_real = self.setup_edms()
                calibration_instance = calibration.PsoCalibration(
                    device_list=self.devices,
                    edm_measured=edm_measured,
                    edm_real=edm_real,
                )
            case "Antenna Calibration (PSO) - ADS":
                edm_measured, edm_real = self.setup_edms()
                calibration_instance = calibration.PsoCalibration(
                    device_list=self.devices,
                    edm_measured=edm_measured,
                    edm_real=edm_real,
                )
            case _:
                raise ValueError(
                    f"Invalid calibration type: {self.calibration_type}"
                )

        if calibration_instance is not None:
            result = await calibration_instance.start_calibration_calc()
            result = await calibration_instance.calc_delays(result)
            logger.info(f"Calc Results: {result}")
        else:
            result = -1
        return result

    async def setup_edms(self) -> Tuple[np.ndarray, np.ndarray]:
        avg_distances = []
        real_distances = []
        for initiator in self.devices:
            for responder in self.devices:
                if responder != initiator:
                    distances = await self.filter_distances(
                        initiator, responder
                    )
                    avg_distance = np.mean(distances)
                    avg_distance = calibration.utils.convert_distance_to_tof(
                        avg_distance
                    )
                    avg_distances.append(avg_distance)

                    real_distance = self.filter_real_distances(
                        initiator, responder
                    )
                    real_distance = calibration.utils.convert_distance_to_tof(
                        real_distance
                    )
                    real_distances.append(real_distance)
                else:
                    avg_distances.append(0)
                    real_distances.append(0)

        edm_measured = calibration.utils.convert_list_to_matrix(
            self.devices, avg_distances
        )
        edm_real = calibration.utils.convert_list_to_matrix(
            self.devices, real_distances
        )
        return edm_measured, edm_real

    async def filter_distances(self, initiator, responder) -> np.ndarray:
        filtered_distances = np.array(
            distance
            for distance in self.distances
            if distance.initiator_id == initiator
            and distance.responder_id == responder
        )
        return filtered_distances

    async def filter_real_distances(self, initiator, responder) -> np.ndarray:
        filtered_distances = np.array(
            distance
            for distance in self.cali_distances
            if distance.initiator_id == initiator
            and distance.responder_id == responder
        )
        return filtered_distances

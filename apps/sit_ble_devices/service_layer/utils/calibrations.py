import logging
from typing import Tuple

import numpy as np
from sit_ble_devices.domain.model import calibration
from sit_ble_devices.models.devices import CalibrationsDistances
from sit_ble_devices.models.distances import DistanceMeasurement
from sit_ble_devices.service_layer.utils.calibration import (
    DecaCalibration,
    PsoCalibration,
)

logger = logging.getLogger("service_layer.utils")


async def start_calibration(
    calibration_dom: calibration.Calibrations,
) -> list[float]:
    calibration_instance = None
    match calibration_dom.calibration_type:
        case "Antenna Calibration (ASP014)":
            edm_measured, edm_real = setup_edms(calibration_dom)
            calibration_instance = DecaCalibration(
                device_list=calibration_dom.devices,
                edm_measured=edm_measured,
                edm_real=edm_real,
            )
        case "Antenna Calibration (PSO)":
            calibration_instance = PsoCalibration(
                device_list=calibration_dom.devices,
                edm_measured=edm_measured,
                edm_real=edm_real,
            )
        case _:
            raise ValueError(
                f"Invalid calibration type: {calibration_dom.calibration_type}"
            )

    if calibration_instance is not None:
        result = await calibration_instance.start_calibration_calc()
        result = await calibration_instance.calc_delays(result)
        logger.info(f"Calc Results: {result}")
    else:
        result = -1
    return result


async def setup_edms(
    calibration_dom: calibration.Calibrations,
) -> Tuple[np.ndarray, np.ndarray]:
    avg_distances = []
    real_distances = []
    for initiator in calibration_dom.devices:
        for responder in calibration_dom.devices:
            if responder != initiator:
                distances = await get_distances(
                    calibration_dom.calibration_id, initiator, responder
                )
                avg_distance = np.mean(distances)
                avg_distance = convert_distance_to_tof(avg_distance)
                avg_distances.append(avg_distance)

                real_distance = get_real_distance(
                    calibration_dom.calibration_id, initiator, responder
                )
                real_distance = convert_distance_to_tof(real_distance)
                real_distances.append(real_distance)
            else:
                avg_distances.append(0)
                real_distances.append(0)

    edm_measured = convert_list_to_matrix(
        calibration_dom.devices, avg_distances
    )
    edm_real = convert_list_to_matrix(calibration_dom.devices, real_distances)
    return edm_measured, edm_real


async def get_distances(calibration_id, initiator, responder) -> np.ndarray:
    results = await DistanceMeasurement.objects.filter(
        calibration__id=calibration_id,
        initiator__device_id=initiator,
        responder__device_id=responder,
    ).afirst()
    distances = np.array(results.values_list("distance"))
    return distances


async def get_real_distance(
    calibration_id, initiator, responder
) -> np.ndarray:
    results = await CalibrationsDistances.objects.filter(
        calibration__id=calibration_id,
        initiator__device_id=initiator,
        responder__device_id=responder,
    ).afirst()
    distances = np.array(results.values_list("distance"))
    return distances


async def convert_distance_to_tof(distances: float) -> float:
    return (1 / 299702547) * distances


async def convert_tof_to_distance(distances: float) -> float:
    return 299702547 * distances


async def convert_list_to_matrix(device_list, distance_list) -> np.ndarray:
    len_devices = len(device_list)
    matrix = np.empty((len_devices, len_devices))
    for list_index, distance in enumerate(distance_list):
        zeile = list_index // len_devices
        spalte = list_index % len_devices
        matrix[zeile, spalte] = distance
    return matrix

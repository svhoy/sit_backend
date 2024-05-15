import numpy as np


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

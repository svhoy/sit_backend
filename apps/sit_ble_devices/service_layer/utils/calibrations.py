import numpy as np
from sit_ble_devices.domain.model import calibration
from sit_ble_devices.models.devices import CalibrationsDistances
from sit_ble_devices.models.distances import DistanceMeasurement


async def start_calibration(
    calibration_dom: calibration.Calibrations,
) -> list[float]:
    calibration_instance = None
    if calibration_dom.calibration_type == "Antenna Calibration (ASP014)":
        calibration_instance = DecaCalibration(calibration_dom)

    if calibration is not None:
        result = await calibration_instance.calibration_calc()
    else:
        result = -1
    return result


# Get Functions
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


class DecaCalibration:
    def __init__(self, calibration_dom: calibration.Calibrations):
        self.calibration = calibration_dom
        self.iterations = 100
        self.avg_distance = []
        self.real_distance = []
        self.edm_measured = np.matrix([])
        self.edm_real = np.matrix([])
        self.events = []
        self.inital_delay = 513e-9
        self.perturbation_limit = 0.2e-9
        self.num_candidates = 1000

    async def calibration_calc(self):
        candidates = np.zeros((self.num_candidates, 4))
        best_canidate = []
        self.setup_edms()
        for i in range(self.iterations):
            print("Running")
            candidates = await self.populate_candidates(i, candidates)
            candidates = await self.evaluate_candidates(candidates)

        best_canidate = candidates[0]
        return await self.calc_delays(best_canidate)

    async def calc_delays(self, candidates):
        result = []
        for idx, device_id in enumerate(self.calibration.devices):
            tx_ant_dly = candidates[idx] * 0.44  # APS014 TX is 44%
            rx_ant_dly = candidates[idx] * 0.56  # APS014 RX is 56%
            result.append([device_id, tx_ant_dly, rx_ant_dly])
        return result

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
                # print(f"Kandidaten Matrix {edm_candidate}")
                norm_diff = np.linalg.norm(self.edm_real - edm_candidate)
                candidates[index, 3] = norm_diff
                # print(f"Differnz Norm: {norm_diff}")
                # print(f"Candidate: {candidate}")

        sorted_indices = np.argsort(candidates[:, 3])
        sorted_candidates = candidates[sorted_indices]
        # print(f"Sorted Candidate: {sorted_candidates}")
        return sorted_candidates

    async def find_best_candidate(self, candidates: np.ndarray):
        return candidates[0]

    # Utils Functions to convert distance data to tof and matrix
    async def setup_edms(self):
        for initiator in self.calibration.devices:
            for responder in self.calibration.devices:
                if responder != initiator:
                    distances = await get_distances(
                        self.calibration.calibration_id, initiator, responder
                    )
                    avg_distance = np.mean(distances)
                    avg_distance = self.convert_distance_to_tof(avg_distance)
                    self.avg_distance.append(avg_distance)

                    real_distance = get_real_distance(
                        self.calibration.calibration_id, initiator, responder
                    )
                    real_distance = self.convert_distance_to_tof(real_distance)
                    self.real_distance.append(real_distance)
                else:
                    self.avg_distance.append(0)
                    self.real_distance.append(0)

        self.edm_measured = self.convert_list_to_matrix(self.avg_distance)
        self.edm_real = self.convert_list_to_matrix(self.real_distance)

    async def convert_distance_to_tof(self, distances: float) -> float:
        return (1 / 299702547) * distances

    async def convert_list_to_matrix(self, distance_list) -> np.ndarray:
        len_devices = len(self.calibration.devices)
        matrix = np.empty((len_devices, len_devices))
        zeile = 0
        for list_index in enumerate(distance_list):
            spalte = list_index % len_devices
            if spalte == 0 and list_index != 0:
                zeile += 1

            matrix[zeile, spalte] = distance_list[list_index]

        return matrix

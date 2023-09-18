import numpy as np

from apps.sit_ble_devices.models.devices import CalibrationsDistances
from sit_ble_devices.models.distances import DistanceMeasurement


class Calibration:
    def __init__(
        self,
        calibration_id=None,
    ):
        self.claibration_id = calibration_id
        self.devices = []
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
        candidates = np.empty((self.num_candidates))
        best_canidate = 0
        self.setup_edms()
        for i in range(self.iterations):
            candidates = await self.populate_candidates(i, candidates)
            candidates = await self.evaluate_candidates(candidates)

        # return find_best_canidate()
        return best_canidate

    async def convert_distance_to_tof(self, distances: float) -> float:
        return (1 / 299702547) * distances

    async def populate_cadidates(self, iteration, candidates) -> np.ndarray:
        if iteration == 0:
            arr = np.random.uniform(
                (self.inital_delay - 6e-9),
                (self.inital_delay + 6e-9),
                self.num_candidates,
            )
        else:
            copied_elements = candidates.size // 4
            best_25 = candidates[:copied_elements]

            randomized_data = best_25 + np.random.uniform(
                -self.perturbation_limit,
                self.perturbation_limit,
                best_25.size * 3,
            )
            arr = np.concatenate([best_25, randomized_data])

        if iteration % 20 == 0 and iteration != 0:
            self.perturbation_limit = self.perturbation_limit // 2

        return arr

    async def evaluate_candidates(self):
        pass

    async def finde_best_candidate(self):
        pass

    async def setup_edms(self):
        for initiator in self.devices:
            for responder in self.devices:
                if responder != initiator:
                    distances = await self.get_distances(initiator, responder)
                    avg_distance = np.mean(distances)
                    avg_distance = self.convert_distance_to_tof(avg_distance)
                    print(avg_distance)
                    self.avg_distance.append(avg_distance)

                    real_distance = self.get_real_distance(
                        initiator, responder
                    )
                    real_distance = self.convert_distance_to_tof(real_distance)
                    self.real_distance.append(real_distance)
                else:
                    self.avg_distance.append(0)
                    self.real_distance.append(0)

        self.edm_measured = self.convert_list_to_matrix(self.avg_distance)
        self.edm_real = self.convert_list_to_matrix(self.real_distance)

    async def get_distances(self, initiator, responder) -> np.ndarray:
        results = await DistanceMeasurement.objects.filter(
            calibration__id=self.claibration_id,
            initiator__device_id=initiator,
            responder__device_id=responder,
        ).afirst()
        distances = np.array(results.values_list("distance"))
        return distances

    async def get_real_distance(self, initiator, responder) -> np.ndarray:
        results = await CalibrationsDistances.objects.filter(
            calibration__id=self.claibration_id,
            initiator__device_id=initiator,
            responder__device_id=responder,
        ).afirst()
        distances = np.array(results.values_list("distance"))
        return distances

    async def convert_list_to_matrix(self, list) -> np.ndarray:
        len_devices = len(self.devices)
        matrix = np.empty((len_devices, len_devices))
        zeile = 0
        for list_index in range(0, len(list)):
            spalte = list_index % len_devices
            if spalte == 0 and list_index != 0:
                zeile += 1

            matrix[zeile, spalte] = list[list_index]

        return matrix

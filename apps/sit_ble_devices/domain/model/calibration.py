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
        self.initiator_device_id = initiator_id
        self.responder_device_id = responder_id
        self.distance = distance


class Calibrations:
    def __init__(self, devices, calibration_id=None, calibration_type=None):
        self.calibration_id = calibration_id
        self.calibration_type = calibration_type
        self.devices = devices
        self.cali_distances = []
        self.events = []

    def append_cali_distances(self, cali_distance_dom: CalibrationDistance):
        self.cali_distances.append(cali_distance_dom)

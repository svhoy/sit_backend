class DistanceMeasurement:
    def __init__(
        self,
        initiator,
        responder,
        sequence,
        measurement,
        distance,
        nlos=None,
        rssi=None,
        fpi=None,
        edistance=None,
        test_id=None,
        calibration_id=None,
    ):
        self.test_id = test_id
        self.claibration_id = calibration_id
        self.initiator = initiator
        self.responder = responder
        self.sequence = sequence
        self.measurement = measurement
        self.distance = distance
        self.nlos = nlos
        self.rssi = rssi
        self.fpi = fpi
        self.edistance = edistance
        self.events = []

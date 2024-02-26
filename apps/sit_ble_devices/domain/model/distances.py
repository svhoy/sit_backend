class DistanceMeasurement:
    def __init__(
        self,
        initiator_id,
        responder_id,
        measurement_type,
        sequence,
        measurement,
        distance,
        time_round_1,
        time_round_2,
        time_reply_1,
        time_reply_2,
        nlos_final=None,
        rssi_final=None,
        fpi_final=None,
        edistance=None,
        test_id=None,
        calibration_id=None,
    ):
        self.test_id = test_id
        self.claibration_id = calibration_id
        self.initiator_id = initiator_id
        self.responder_id = responder_id
        self.measurement_type = measurement_type
        self.sequence = sequence
        self.measurement = measurement
        self.distance = distance
        self.time_round_1 = time_round_1
        self.time_round_2 = time_round_2
        self.time_reply_1 = time_reply_1
        self.time_reply_2 = time_reply_2
        self.nlos_final = nlos_final
        self.rssi_final = rssi_final
        self.fpi_final = fpi_final
        self.edistance = edistance
        self.events = []

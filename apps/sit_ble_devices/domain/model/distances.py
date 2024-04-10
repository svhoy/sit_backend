class DistanceMeasurement:
    def __init__(
        self,
        measurement_type,
        sequence,
        measurement,
        distance,
        **kwargs,
    ):
        self.measurement_id = kwargs.get("measurement_id", None)
        self.test_id = kwargs.get("test_id", None)
        self.calibration_id = kwargs.get("calibration_id", [])
        self.initiator_id = kwargs.get("initiator_id", None)
        self.responder_id = kwargs.get("responder_id", None)
        self.measurement_type = measurement_type
        self.sequence = sequence
        self.measurement = measurement
        self.distance = distance
        self.time_round_1 = kwargs.get("time_round_1", None)
        self.time_round_2 = kwargs.get("time_round_2", None)
        self.time_reply_1 = kwargs.get("time_reply_1", None)
        self.time_reply_2 = kwargs.get("time_reply_2", None)
        self.nlos_final = kwargs.get("nlos_final", None)
        self.rssi_final = kwargs.get("rssi_final", None)
        self.fpi_final = kwargs.get("fpi_final", None)
        self.edistance = kwargs.get("edistance", None)
        self.events = []

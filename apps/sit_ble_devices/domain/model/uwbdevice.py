class AntDelay:
    def __init__(
        self,
        calibration_id,
        device_id,
        tx_ant_delay,
        rx_ant_delay,
        **kwargs,
    ):
        self.ant_delay_id = kwargs.get("ant_delay_id", None)
        self.changed = kwargs.get("changed", None)
        self.calibration_id = calibration_id
        self.default = kwargs.get("default", False)
        self.device_id = device_id
        self.tx_ant_delay = tx_ant_delay
        self.rx_ant_delay = rx_ant_delay


class UwbDevice:
    def __init__(self, device_id, device_name, comments):
        self.device_id = device_id
        self.device_name = device_name
        self.comments = comments
        self.ant_delay = []
        self.events = []

    def append_ant_delay(self, ant_delay_dom: AntDelay):
        self.ant_delay.append(ant_delay_dom)

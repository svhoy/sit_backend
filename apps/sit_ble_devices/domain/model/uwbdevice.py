class AntDelay:
    def __init__(
        self,
        default,
        calibration_id,
        device_id,
        tx_ant_delay,
        rx_ant_delay,
        ant_delay_id=None,
        changed=None,
    ):
        self.ant_delay_id = ant_delay_id
        self.changed = changed
        self.calibration_id = calibration_id
        self.default = default
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

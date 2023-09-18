from dataclasses import dataclass, asdict
from json import dumps


@dataclass
class Command:
    @property
    def __dict__(self):
        dict = {}
        dict["type"] = self.__class__.__name__
        dict["data"] = asdict(self)
        return dict

    @property
    def json(self):
        return dumps(self.__dict__)


@dataclass
class RegisterWsClient(Command):
    client_id: str
    room_name: str = None


@dataclass
class UnregisterWsClient(Command):
    room_name: str


@dataclass
class ConnectBleDevice(Command):
    device_id: str


@dataclass
class DisconnectBleDevice(Command):
    device_id: str


@dataclass
class RegisterBleConnection(Command):
    device_id: str


@dataclass
class UnregisterBleConnection(Command):
    device_id: str


@dataclass
class StartCalibration(Command):
    devices: list[str]


@dataclass
class StartDistanceMeasurement(Command):
    initiator: str
    responder: str


@dataclass
class StopDistanceMeasurement(Command):
    pass


@dataclass
class SaveMesurement(Command):
    initiator: str
    sequence: int
    measurement: int
    distance: float
    nlos: int
    rssi: float
    fpi: float


@dataclass
class StartTestMeasurement(Command):
    test_id: int
    initiator: str
    responder: list[str]
    min_measurement: int
    max_measurement: int


@dataclass
class StopTestMeasurement(Command):
    pass


@dataclass
class SaveTestMeasurement(Command):
    test_id: int
    initiator: str
    sequence: int
    distance: float
    nlos: int
    rssi: float
    fpi: float


@dataclass
class StartCalibrationMeasurement(Command):
    calibration_id: int
    devices: list[str]
    max_measurement: int
    rx_ant_dly: int = 0
    tx_ant_dly: int = 0


@dataclass
class SaveCalibrationMeasurement(Command):
    calibration: int
    initiator: str
    sequence: int
    distance: float
    nlos: int
    rssi: float
    fpi: float


@dataclass
class PositionMeasurement(Command):
    pass

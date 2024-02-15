from dataclasses import asdict, dataclass
from json import dumps


@dataclass
class Command:
    @property
    def __dict__(self):
        dict_buf = {}
        dict_buf["type"] = self.__class__.__name__
        dict_buf["data"] = asdict(self)
        return dict_buf

    @property
    def json(self):
        return dumps(self.__dict__)


@dataclass
class RegisterWsClient(Command):
    client_id: str
    room_name: str = ""


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
class CreateCalibration(Command):
    calibration_type: str
    measurement_type: str
    devices: list[str]


@dataclass
class AddCalibrationDistances(Command):
    calibration_id: int
    distance_list: list[tuple[str, str, int]]


@dataclass
class StartCalibrationCalc(Command):
    calibration_id: str


@dataclass
class StartDistanceMeasurement(Command):
    initiator: str
    responder: str
    measurement_type: str


@dataclass
class StopDistanceMeasurement(Command):
    pass


@dataclass
class SaveMesurement(Command):
    initiator: str
    responder: str
    measurement_type: str
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
    measurement_type: str
    min_measurement: int
    max_measurement: int
    rx_ant_dly: int = 0
    tx_ant_dly: int = 0


@dataclass
class StopTestMeasurement(Command):
    pass


@dataclass
class SaveTestMeasurement(Command):
    test_id: int
    initiator: str
    responder: str
    measurement_type: str
    sequence: int
    measurement: int
    distance: float
    nlos: int
    rssi: float
    fpi: float


@dataclass
class StartCalibrationMeasurement(Command):
    calibration_id: int
    devices: list[str]
    measurement_type: str = (
        "ds_3_twr"  # set ds-twr to default because it is the better way to measure distance
    )
    max_measurement: int = 200
    rx_ant_dly: int = 0
    tx_ant_dly: int = 0


@dataclass
class SaveCalibrationMeasurement(Command):
    calibration_id: int
    initiator: str
    responder: str
    measurement_type: str
    sequence: int
    measurement: int
    distance: float
    nlos: int
    rssi: float
    fpi: float


@dataclass
class PositionMeasurement(Command):
    pass

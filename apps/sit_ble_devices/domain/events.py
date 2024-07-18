from dataclasses import asdict, dataclass, field
from json import dumps
from msilib import sequence


@dataclass
class Event:  # pylint: disable=duplicate-code
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
class WsClientRegisterd(Event):
    clients: list[str]


@dataclass
class WsClientUnregisterd(Event):
    room_id: str


@dataclass
class BleDeviceConnected(Event):
    device_id: str


@dataclass
class BleDeviceRegistered(Event):
    device_list: list[str]
    new_device: str


@dataclass
class BleDeviceUnregistered(Event):
    device_list: list[str]
    device: str


@dataclass
class BleDeviceConnectFailed(Event):
    device_id: str
    reason: str = ""


@dataclass
class BleDeviceConnectError(Event):
    device_id: str
    reason: str = ""


@dataclass
class BleDeviceDisconnected(Event):
    room_id: str


@dataclass
class MeasurementSaved(Event):
    initiator: str | None
    sequence: int
    distance: float
    nlos: int
    rssi: float
    fpi: float
    e_distance: float | None = None


@dataclass
class MeasurementListSaved(Event):
    test_id: int
    measurements: int


@dataclass
class TestFinished(Event):
    test_id: int


@dataclass
class CalibrationMeasurementSaved(Event):
    measurement: int
    sequence: int
    devices: list[str] = field(default_factory=list)


@dataclass
class CalibrationCreated(Event):
    calibration_id: int


@dataclass
class CalibrationInitFinished(Event):
    calibration_id: int
    calibration_type: str
    measurement_type: str
    devices: list[str] = field(default_factory=list)


@dataclass
class CalibrationCopied(Event):
    calibration_id: int
    calibration_type: str


@dataclass
class CalibrationSimpleCopied(Event):
    calibration_id: int
    calibration_type: str


@dataclass
class CalibrationSimpleMeasurementFinished(Event):
    calibration_id: int


@dataclass
class CalibrationMeasurementFinished(Event):
    calibration_id: int


@dataclass
class CalibrationCalcFinished(Event):
    calibration_id: int
    result: list[tuple[str, float, float]]


@dataclass
class CalibrationResultsSaved(Event):
    calibration_id: int


@dataclass
class AddedUwbDevice(Event):
    device_name: str
    device_id: str


@dataclass
class AddedAntDelay(Event):
    calibration_id: int
    device_id: str
    tx_ant_dly: float
    rx_ant_dly: float

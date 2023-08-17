from dataclasses import dataclass, asdict
from json import dumps
from types import NoneType


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
    initiator: str | None = None
    responder: str | None = None
    test_id: str | None = None
    min_measurements: int | None = None
    max_measurements: int | None = None


@dataclass
class StopDistanceMeasurement(Command):
    pass


@dataclass
class SaveMesurement(Command):
    initiator: str
    sequence: int
    distance: float
    nlos: int
    rssi: float
    fpi: float


@dataclass
class PositionMeasurement(Command):
    pass

from dataclasses import dataclass, asdict
from json import dumps


@dataclass
class Event:
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
    reason: str = None


@dataclass
class BleDeviceConnectError(Event):
    device_id: str
    reason: str = None


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

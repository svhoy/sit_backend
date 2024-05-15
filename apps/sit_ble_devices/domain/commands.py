from dataclasses import asdict, dataclass
from json import dumps
from math import e

from apps.sit_ble_devices.domain.model import calibration


@dataclass
class Command:  # pylint: disable=duplicate-code
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
class CopieCalibration(Command):
    copie_calibration_id: int
    calibration_type: str


@dataclass
class CopieSimpleCalibration(Command):
    copie_calibration_id: int
    calibration_type: str


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
    time_round_1: float
    time_round_2: float
    time_reply_1: float
    time_reply_2: float
    nlos_final: int
    rssi_final: float
    fpi_final: float


@dataclass
class StartTestMeasurement(Command):
    test_id: int
    initiator: str
    responder: list[str]
    measurement_type: str
    min_measurement: int
    max_measurement: int
    init_rx_ant_dly: float = 0
    init_tx_ant_dly: float = 0
    resp_rx_ant_dly: float = 0
    resp_tx_ant_dly: float = 0


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
    time_round_1: float
    time_round_2: float
    time_reply_1: float
    time_reply_2: float
    nlos_final: int
    rssi_final: float
    fpi_final: float


@dataclass
class StartCalibrationMeasurement(Command):
    calibration_id: int
    devices: list[str]
    # set ds-twr to default because it is the better way
    # to measure distance
    measurement_type: str = "ds_3_twr"
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
    time_round_1: float
    time_round_2: float
    time_reply_1: float
    time_reply_2: float
    nlos_final: int
    rssi_final: float
    fpi_final: float


@dataclass
class StartSimpleCalibrationMeasurement(Command):
    calibration_id: int
    devices: list[str]
    measurement_type: str = "two_device"
    max_measurement: int = 200
    rx_ant_dly: int = 0
    tx_ant_dly: int = 0


@dataclass
class SaveSimpleCalibrationMeasurement(Command):
    calibration_id: int
    sequence: int
    measurement: int
    devices: list[str]
    time_m21: float
    time_m31: float
    time_a21: float
    time_a31: float
    time_b21: float
    time_b31: float
    time_tc_i: float
    time_tc_ii: float
    time_tb_i: float
    time_tb_ii: float
    time_round_1: float
    time_round_2: float
    time_reply_1: float
    time_reply_2: float
    distance: float


@dataclass
class PositionMeasurement(Command):
    pass


@dataclass
class StartDebugCalibration(Command):
    calibration_id: int
    devices: list[str]
    measurement_type: str = "simple"
    max_measurement: int = 0
    rx_ant_dly: int = 0
    tx_ant_dly: int = 0
    calibration_type: str = "simple_calibration"

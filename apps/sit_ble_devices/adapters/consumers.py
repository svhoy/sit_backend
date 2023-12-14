# Standard Library
import importlib.util
import json
import pkgutil

from asgiref.sync import sync_to_async

# Third Party
from channels.generic.websocket import AsyncWebsocketConsumer

from sit_ble_devices import bootstrap
from sit_ble_devices.domain import commands
from sit_ble_devices.models import DeviceTests, DistanceMeasurement
from sit_ble_devices.service_layer import uow

bus = bootstrap.bootstrap(
    uow=uow.UnitOfWork(),
    duow=uow.DistanceUnitOfWork(),
    cuow=uow.CalibrationUnitOfWork(),
    uduow=uow.UwbDeviceUnitOfWork(),
)


class BleDeviceConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._test_id = None
        self.dataclasses = self.find_dataclasses_in_directory()

    async def connect(self):
        self.room_group_name = (
            "sit_" + self.scope["url_route"]["kwargs"]["room_id"]
        )

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()
        await self.send(
            text_data=json.dumps({"type": "ConnectionEstablished", "data": {}})
        )

    async def disconnect(self, code):
        message = commands.UnregisterWsClient(self.room_group_name)
        await bus.handle(message)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = self.create_dataclass_instance(data["type"], data["data"])
        await bus.handle(message)

    async def send_command(self, event):
        await self.send(text_data=event["data"])

    async def send_event(self, event):
        await self.send(text_data=event["data"])

    def create_dataclass_instance(self, event_type, data):
        data_class = self.dataclasses.get(event_type)
        if data_class:
            instance = data_class(**data)
            return instance
        else:
            raise ValueError("Invalid event type")

    def find_dataclasses_in_directory(self):
        dataclasses = {}
        directory = (
            "sit_ble_devices.domain"  # Vollständiger Pfad zu den Klassen
        )

        try:
            package = importlib.import_module(directory)
        except ModuleNotFoundError:
            return dataclasses  # Module not found, return empty dict

        for importer, modname, ispkg in pkgutil.walk_packages(
            path=package.__path__, prefix=package.__name__ + "."
        ):
            module = importlib.import_module(modname)
            for name, obj in module.__dict__.items():
                if (
                    isinstance(obj, type)
                    and hasattr(obj, "__annotations__")
                    and hasattr(obj, "__dataclass_fields__")
                ):
                    dataclasses[name] = obj

        return dataclasses

    ##########################################################
    ##########################################################
    ##########################################################
    # TODO: OLD Functions should be replaced in event handler

    # Distance Messages
    async def handle_distance_msg(self, data, setup=None):
        match data:
            case {
                "state": "start" as state,
                "test_id": test_id,
            }:
                self._test_id = test_id
                if setup is None:
                    setup = await sync_to_async(self.set_setup)(
                        data["test_id"]
                    )
                data = {"state": state, "test_id": test_id}
                await self.send_distance(data, setup)
            case {
                "state": "stop" as state,
                "test_id": test_id,
            }:
                self._test_id = None
                data = {"state": state, "test_id": test_id}
                print("Test")
                await self.send_distance(data)
            case {
                "state": "scanning" as state,
                "test_id": test_id,
                "sequence": sequence,
                "distance": distance,
                "nlos": nlos,
                "rssi": rssi,
                "fpi": fpi,
            }:
                error_distance = await sync_to_async(self.save_distance)(
                    test_id,
                    sequence,
                    distance,
                    nlos,
                    rssi,
                    fpi,
                )
                data = {
                    "state": state,
                    "test_id": test_id,
                    "sequence": sequence,
                    "distance": distance,
                    "nlos": nlos,
                    "rssi": rssi,
                    "fpi": fpi,
                    "error_distance": error_distance,
                }
                await self.send_distance(data, setup)

    def set_setup(self, test_id):
        test = DeviceTests.objects.get(pk=test_id)
        setup = {
            "initiator_device": test.initiator_device.device_id,
            "responder_device": test.responder_device.device_id,
        }
        return setup

    def save_distance(self, test_id, sequence, distance, nlos, rssi, fpi):
        device_test = None
        error_distance = None
        if test_id is not None:
            device_test = DeviceTests.objects.get(id=test_id)
            if device_test.real_test_distance is not None:
                error_distance = distance - device_test.real_test_distance
        distance_model = DistanceMeasurement.objects.create(
            test=device_test,
            sequence=sequence,
            distance=distance,
            nlos=nlos,
            RecivedSignalStrengthIndex=rssi,
            firstPathIndex=fpi,
            error_distance=error_distance,
        )
        distance_model.save()
        return error_distance

    async def send_distance(
        self,
        data,
        setup=None,
    ):
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "distance_msg", "data": data, "setup": setup},
        )

    async def distance_msg(self, event):
        data = event["data"]
        setup = event["setup"]
        msg = json.dumps(
            {"type": "distance_msg", "data": data, "setup": setup}
        )
        await self.send(text_data=msg)

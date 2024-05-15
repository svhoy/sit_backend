# Standard Library
import importlib.util
import json
import logging
import pkgutil

# Third Party
from channels.generic.websocket import AsyncWebsocketConsumer
from sit_ble_devices import bootstrap
from sit_ble_devices.service_layer import uow

# create logger
logger = logging.getLogger("consumer")

bus = bootstrap.bootstrap(
    uow=uow.UnitOfWork(),
    duow=uow.DistanceUnitOfWork(),
    cuow=uow.CalibrationUnitOfWork(),
    uduow=uow.UwbDeviceUnitOfWork(),
    cmuow=uow.CalibrationMeasurementUnitOfWork(),
)


class BleDeviceConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._test_id = None
        self.dataclasses = self.find_dataclasses_in_directory()
        self.room_group_name = ""

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

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        logger.debug(f"Recived Date: {data}")
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

        for (
            importer,  # pylint: disable=unused-variable
            modname,
            ispkg,  # pylint: disable=unused-variable
        ) in pkgutil.walk_packages(
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

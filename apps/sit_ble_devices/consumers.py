# Standard Library
import json

from asgiref.sync import sync_to_async

# Third Party
from channels.generic.websocket import AsyncWebsocketConsumer
from sit_ble_devices.models import DeviceTests, DistanceMeasurement

from .store.store import Store


class BleDeviceConsumer(AsyncWebsocketConsumer):
    _test_id = None

    async def connect(self):
        self.room_group_name = "ble_device"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "connected": True,
                }
            )
        )

    async def disconnect(self, code):
        json_store = Store()
        connection_list = []
        connection_list.extend(
            json_store.get_value("websocket_connection", [])
        )
        connection_list.clear()
        json_store.set_value("websocket_connection", connection_list)
        json_store.save()
        await self.send_connection_ping()

    async def receive(self, text_data):
        data = json.loads(text_data)
        match data:
            case {"type": "scanning_state", "scan": scan}:
                await self.scanning_state(scan)
            case {"type": "connection_register", "device_id": device_id}:
                await self.connection_register(device_id)
            case {"type": "connection_ping", "device_id": device_id}:
                await self.connection_register(device_id)
            case {"type": "distance_msg", "data": data}:
                await self.handle_distance_msg(data)

    async def scanning_state(self, scan_data):
        match scan_data:
            case {"state": True as state, "device_name": device_name}:
                await self.send_start_scanning_msg(
                    state, "Scanning for Device ", device_name
                )
            case {
                "state": False as state,
                "connection": "complete" as connection,
                "device_name": device_name,
            }:
                await self.device_completion(device_name, connection)
            case {
                "state": False as state,
                "connection": "error" as connection,
                "device_name": device_name,
            }:
                await self.send_connection_msg(
                    False,
                    "Connection Error with " + device_name,
                    device_name,
                    connection,
                )
            case {
                "state": False as state,
                "connection": "notFound" as connection,
                "device_name": device_name,
            }:
                await self.send_connection_msg(
                    False,
                    device_name + "not found",
                    device_name,
                    connection,
                )
            case {
                "state": False as state,
                "connection": "disconnect" as connection,
                "device_name": device_name,
            }:
                await self.disconnect_ble_device(device_name, connection)

    # Manage Bluetooth Connections
    async def send_start_scanning_msg(self, state, message, device):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "scanning_msg",
                "state": state,
                "message": message,
                "device_name": device,
            },
        )

    async def scanning_msg(self, event):
        state = event["state"]
        message = event["message"]
        device = event["device_name"]
        print(device)
        await self.send(
            text_data=json.dumps(
                {
                    "type": "scanning_state",
                    "scan": {
                        "state": state,
                        "message": message + device + "...",
                        "device_name": device,
                    },
                }
            )
        )

    async def device_completion(self, device_name, connection):
        json_store = Store()
        device_list = json_store.get_value("device_list", [])
        device_set = set(device_list)
        device_set.add(device_name)
        json_store.set_value("device_list", list(device_set))
        json_store.save()
        await self.send_connection_msg(
            False,
            "Connection Complete",
            device_name,
            connection,
        )

    async def disconnect_ble_device(self, device_name, connection):
        json_store = Store()
        device_list = []
        device_list.extend(json_store.get_value("device_list", []))
        if device_name in device_list:
            device_list.remove(device_name)
        json_store.set_value("device_list", device_list)
        json_store.save()
        await self.send_connection_msg(
            False,
            device_name + " disconnected",
            device_name,
            connection,
        )

    async def send_connection_msg(
        self, state, message, device_name, connection
    ):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "connection_msg",
                "state": state,
                "message": message,
                "connection": connection,
                "device_name": device_name,
            },
        )

    async def connection_msg(self, event):
        state = event["state"]
        message = event["message"]
        connection = event["connection"]
        device_name = event["device_name"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "scanning_state",
                    "scan": {
                        "state": state,
                        "message": message,
                        "connection": connection,
                        "device_name": device_name,
                    },
                }
            )
        )

    # Manage Webserver Connections
    async def connection_register(self, device_id):
        json_store = Store()
        websocket_connections = json_store.get_value(
            "websocket_connection", []
        )
        connection_set = set(websocket_connections)
        connection_set.add(device_id)
        json_store.set_value("websocket_connection", list(connection_set))
        json_store.save()
        await self.send_connection_update(
            json_store.get_value("websocket_connection"),
            json_store.get_value("device_list", []),
        )

    async def send_connection_update(
        self,
        connection_list,
        device_list,
    ):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "connection_update_msg",
                "connection_list": connection_list,
                "device_list": device_list,
            },
        )

    async def connection_update_msg(self, event):
        connection_list = event["connection_list"]
        device_list = event["device_list"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection_update",
                    "connection_list": connection_list,
                    "device_list": device_list,
                }
            )
        )

    async def send_connection_ping(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "connection_ping_msg",
            },
        )

    async def connection_ping_msg(self, event):
        await self.send(text_data=json.dumps({"type": "connection_ping"}))

    # Distance Messages
    async def handle_distance_msg(self, data):
        match data:
            case {
                "state": "start" as state,
                "test_id": test_id,
            }:
                self._test_id = test_id
                await self.send_distance(state, -1, test_id)
            case {
                "state": "stop" as state,
                "test_id": test_id,
            }:
                self._test_id = None
                await self.send_distance(state, -1, test_id)
            case {
                "state": "scanning" as state,
                "test_id": test_id,
                "sequence": sequence,
                "distance": distance,
                "nlos": nlos,
                "rssi": rssi,
                "fpi": fpi,
            }:
                if distance > -1:
                    error_distance = await sync_to_async(self.save_distance)(
                        test_id,
                        sequence,
                        distance,
                        nlos,
                        rssi,
                        fpi,
                    )
                    await self.send_distance(
                        state, distance, test_id, error_distance
                    )

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
        self, state, distance, test_id, error_distance=None
    ):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "distance_msg",
                "state": state,
                "distance": distance,
                "test_id": test_id,
                "error_distance": error_distance,
            },
        )

    async def distance_msg(self, event):
        distance = event["distance"]
        state = event["state"]
        test_id = event["test_id"]
        error_distance = event["error_distance"]
        msg = json.dumps(
            {
                "type": "distance_msg",
                "data": {
                    "state": state,
                    "distance": distance,
                    "error_distance": error_distance,
                    "test_id": test_id,
                },
            }
        )
        await self.send(text_data=msg)

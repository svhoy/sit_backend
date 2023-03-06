# Standard Library
import json

# Third Party
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class BleDeviceConsumer(AsyncWebsocketConsumer):
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
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        match data:
            case {"type": "scanning_state", "scan": scan}:
                await self.scanning_state(scan)
            case {"type": "connection_register", "device_id": device_id}:
                await self.connection_register(device_id)

    async def scanning_state(self, scan_data):
        match scan_data:
            case {"state": state, "device_name": device_name} if state is True:
                await self.send_start_scanning_msg(
                    state, "Scanning for Device ", device_name
                )
            case {
                "state": state,
                "connection": connection,
                "device_name": device_name,
            } if state is False and connection == "complete":
                await self.send_connection_msg(
                    False,
                    "Connection Complete",
                    device_name,
                    connection,
                )
            case {
                "state": state,
                "connection": connection,
                "device_name": device_name,
            } if state is False and connection == "error":
                await self.send_connection_msg(
                    False,
                    "Connection Error no Device with name DWM3001 Blue found",
                    device_name,
                    connection,
                )

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

    async def connection_register(self, device_id):
        await self.send_connection_update([device_id])

    async def send_connection_update(self, device_list):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "connection_update_msg",
                "device_list": device_list,
            },
        )

    async def connection_update_msg(self, event):
        device_list = event["device_list"]
        await self.send(
            text_data=json.dumps(
                {"type": "connection_update", "device_list": device_list}
            )
        )

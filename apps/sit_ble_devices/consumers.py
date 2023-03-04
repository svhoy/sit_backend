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
            case {"type": "scanning_state", "scan": scan} if scan[
                "state"
            ] is True:
                await self.send_start_scanning_msg(
                    True, "Scanning for Device ", scan["device_name"]
                )
            case {"type": "scanning_state", "scan": scan} if scan[
                "state"
            ] is False and scan["connection"] == "complete":
                await self.send_connection_msg(
                    False,
                    "Connection Complete",
                    scan["device_name"],
                    scan["connection"],
                )
            case {"type": "scanning_state", "scan": scan} if scan[
                "state"
            ] is False and scan["connection"] == "error":
                await self.send_connection_msg(
                    False,
                    "Connection Error no Device with name DWM3001 Blue found",
                    scan["device_name"],
                    scan["connection"],
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

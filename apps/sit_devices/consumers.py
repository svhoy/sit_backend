# Standard Library
import json

# Third Party
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import read_scanning_state, write_scanning_state


class BleScanConsumer(AsyncWebsocketConsumer):
    PATH = "apps/sit_devices/data_cache/scan_cache.json"

    async def connect(self):
        self.room_group_name = "test"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "connected": True,
                    "message": "You are connected to BLE Scan",
                    "scan": {"state": read_scanning_state(self.PATH)},
                }
            )
        )

    async def disconnect(self, code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if "scan" in data and data["scan"]["state"] is True:
            write_scanning_state(self.PATH, True)
            await self.send_scanning_update("Scanning...", None)
        elif "scan" in data and data["scan"]["state"] is False:
            write_scanning_state(self.PATH, False)
            await self.send_scanning_update(
                data["scan"]["message"], data["scan"]["unprovisioned"]
            )

    async def send_scanning_update(self, message, unprovisioned):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "scanning_update",
                "message": message,
                "unprovisioned": unprovisioned,
            },
        )

    async def scanning_update(self, event):
        message = event["message"]
        unprovisioned = event["unprovisioned"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "scanning_state",
                    "scan": {
                        "state": read_scanning_state(self.PATH),
                        "message": message,
                        "unprovisioned": unprovisioned,
                    },
                }
            )
        )

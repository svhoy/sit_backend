# Standard Library
import json

# Third Party
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from .utils import (
    read_scanning_state,
    write_scanning_state,
    read_unprovisioned,
    write_unprovisioned,
)


class BleScanConsumer(AsyncWebsocketConsumer):
    PATH = "apps/sit_devices/data_cache/scan_cache.json"

    async def connect(self):
        self.room_group_name = "scan"

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
        write_unprovisioned(self.PATH, {})
        write_scanning_state(self.PATH, False)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if "scan" in data and data["scan"]["state"] is True:
            write_scanning_state(self.PATH, True)
            await self.send_scanning_update("Scanning...", None)
        elif "scan" in data and data["scan"]["state"] is False:
            write_scanning_state(self.PATH, False)
            write_unprovisioned(self.PATH, data["scan"]["unprovisioned"])
            await self.send_scanning_update(
                data["scan"]["message"], data["scan"]["unprovisioned"]
            )
            test = get_channel_layer()
            await test.group_send(
                "provisioning",
                {
                    "type": "prov_update",
                    "unprovisioned": data["scan"]["unprovisioned"],
                },
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


class BleProvisioning(AsyncWebsocketConsumer):
    PATH = "apps/sit_devices/data_cache/scan_cache.json"

    async def connect(self):
        self.room_group_name = "provisioning"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "connected": True,
                    "message": "You are connected to BLE Provisioning",
                    "scan": {"state": read_scanning_state(self.PATH)},
                }
            )
        )

    async def disconnect(self, code):
        write_unprovisioned(self.PATH, {})
        write_scanning_state(self.PATH, False)

    async def receive(self, text_data):
        data = json.loads(text_data)

    async def send_prov_update(self, message, unprovisioned):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "prov_state",
                "unprovisioned": unprovisioned,
            },
        )

    async def prov_update(self, event):
        unprovisioned = event["unprovisioned"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "prov_state",
                    "scan": {
                        "unprovisioned": unprovisioned,
                    },
                }
            )
        )

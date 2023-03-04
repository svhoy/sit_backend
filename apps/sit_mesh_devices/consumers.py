# Standard Library
import json

# Third Party
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from .utils import (
    read_prov_device,
    read_prov_state,
    read_scanning_state,
    read_unprovisioned,
    write_prov,
    write_scanning_state,
    write_unprovisioned,
)


class BleMeshDeviceConsumer(AsyncWebsocketConsumer):
    PATH = "apps/sit_mesh_devices/data_cache/scan_cache.json"

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
        if read_scanning_state:
            write_scanning_state(self.PATH, False)
            await self.send_scanning_update(
                "Device disconnected, Scanning aborted", None
            )

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
        elif "prov" in data and data["prov"]["state"] is True:
            write_prov(self.PATH, True, data["prov"]["uuid"])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "prov_update",
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

    async def prov_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "prov_update",
                    "prov": {
                        "state": read_prov_state(self.PATH),
                        "uuid": read_prov_device(self.PATH),
                    },
                }
            )
        )

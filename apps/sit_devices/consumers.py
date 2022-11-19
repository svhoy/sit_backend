# Standard Library
import json
import time

# Third Party
from channels.generic.websocket import WebsocketConsumer


class BleScanConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "connected": True,
                    "message": "You are connected to BLE Scan",
                }
            )
        )

    def disconnect(self, code):
        pass

    def receive(self, text_data=None):
        data = json.loads(text_data)
        if "scan" in data and data["scan"] is True:
            self.send(
                text_data=json.dumps(
                    {
                        "type": "scanning_state",
                        "scanning": True,
                        "message": "Scanning...",
                    }
                )
            )

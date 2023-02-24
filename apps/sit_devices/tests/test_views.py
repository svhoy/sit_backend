# Third Party
import pytest

from channels.testing import WebsocketCommunicator

# Library
from config.asgi import application


TEST_CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


@pytest.mark.asyncio
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_connection_message(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()
        message = {
            "type": "connection_established",
            "connected": True,
            "message": "You are connected to BLE Scan",
            "scan": {"state": False},
        }
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_receive_and_send_start_scanning_message(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()
        response = await communicator.receive_json_from()
        start_message = {
            "type": "scanning_state",
            "scan": {"state": True},
        }
        rev_message = {
            "type": "scanning_state",
            "scan": {
                "state": True,
                "message": "Scanning...",
                "unprovisioned": None,
            },
        }
        await communicator.send_json_to(start_message)
        response = await communicator.receive_json_from()
        assert response == rev_message
        await communicator.disconnect()

    async def test_receive_and_send_end_scanning_message(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()
        response = await communicator.receive_json_from()
        lst = [42, 98, 77]
        message = {
            "type": "scanning_state",
            "scan": {
                "state": False,
                "message": "Scan Completed",
                "unprovisioned": lst,
            },
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_receive_and_send_start_prov_message(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()
        response = await communicator.receive_json_from()
        message = {
            "type": "prov_update",
            "prov": {
                "state": True,
                "uuid": 44,
            },
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

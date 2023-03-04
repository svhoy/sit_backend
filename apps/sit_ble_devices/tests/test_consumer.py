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
class TestBleDeviceWebSocket:
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
        }
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_receive_and_send_start_scanning_message_specific_device(
        self, settings
    ):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()
        response = await communicator.receive_json_from()
        start_message = {
            "type": "scanning_state",
            "scan": {"state": True, "device_name": "DWM3001 Blue"},
        }
        rev_message = {
            "type": "scanning_state",
            "scan": {
                "state": True,
                "message": "Scanning for Device DWM3001 Blue...",
                "device_name": "DWM3001 Blue",
            },
        }
        await communicator.send_json_to(start_message)
        response = await communicator.receive_json_from()
        assert response == rev_message
        await communicator.disconnect()

    async def test_receive_and_send_connection_successful_message(
        self, settings
    ):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()
        response = await communicator.receive_json_from()
        message = {
            "type": "scanning_state",
            "scan": {
                "state": False,
                "message": "Connection Complete",
                "connection": "complete",
                "device_name": "DWM3001 Blue",
            },
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_receive_and_send_connection_unsuccessful_message(
        self, settings
    ):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()
        response = await communicator.receive_json_from()
        message = {
            "type": "scanning_state",
            "scan": {
                "state": False,
                "message": "Connection Error no Device with name DWM3001 Blue found",
                "connection": "error",
                "device_name": "",
            },
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

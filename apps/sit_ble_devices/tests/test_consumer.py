# Third Party
import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from sit_ble_devices.models import DistanceMeasurement
from sit_ble_devices.store.store import Store

# Library
from config.asgi import application

TEST_CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


def store_cleanup():
    json_store = Store()
    connection_list = []
    json_store.set_value("websocket_connection", connection_list)
    json_store.set_value("device_list", connection_list)
    json_store.save()


@pytest.fixture(autouse=True)
def clean_store_files():
    # Code that will run before your test, for example:
    store_cleanup()
    # A test function will be run at this point
    yield
    # Code that will run after your test, for example:
    store_cleanup()


@pytest.mark.django_db
@pytest.mark.asyncio
class TestWebSocketConnection:
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

    async def test_device_connection_register(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()

        response = await communicator.receive_json_from()
        send_message = {
            "type": "connection_register",
            "device_id": "Frontend_Sven",
        }
        await communicator.send_json_to(send_message)
        rev_message = {
            "type": "connection_update",
            "connection_list": ["Frontend_Sven"],
            "device_list": [],
        }
        response = await communicator.receive_json_from()
        assert response == rev_message
        await communicator.disconnect()
        Store

    async def test_device_connection_cancel(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        communicator2 = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()
        await communicator2.connect()
        response = await communicator.receive_json_from()
        response = await communicator2.receive_json_from()
        message = {
            "type": "connection_register",
            "device_id": "Test 1",
        }
        message1 = {
            "type": "connection_register",
            "device_id": "Test 2",
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        update_msg = {
            "type": "connection_update",
            "connection_list": ["Test 1"],
            "device_list": [],
        }
        assert update_msg == response
        await communicator.send_json_to(message1)
        response = await communicator.receive_json_from()
        update_msg = {
            "type": "connection_update",
            "connection_list": ["Test 1", "Test 2"],
            "device_list": [],
        }
        update_msg1 = {
            "type": "connection_update",
            "connection_list": ["Test 2", "Test 1"],
            "device_list": [],
        }
        if response["connection_list"] == ["Test 1", "Test 2"]:
            assert update_msg == response
        else:
            assert update_msg1 == response
        await communicator2.disconnect()

        ping_msg = {"type": "connection_ping"}
        response = await communicator.receive_json_from()
        assert response == ping_msg
        await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
class TestBLEDeviceConnection:
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
                "message": "Connection Error with DWM3001 Blue",
                "connection": "error",
                "device_name": "",
            },
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_receive_and_send_device_not_found_message(self, settings):
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
                "message": "Device DWM3001 Blue not found",
                "connection": "notFound",
                "device_name": "",
            },
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_disconnect_ble_device_msg(self, settings):
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
                "message": "Device DWM3001 Blue disconnected",
                "connection": "disconnect",
                "device_name": "DWM3001 Blue",
            },
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
class TestUWBDistanceMeasuring:
    async def test_start_distance_measuring(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()
        response = await communicator.receive_json_from()
        message = {
            "type": "distance_msg",
            "state": "start",
            "distance": -1,
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_stop_distance_measuring(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()
        response = await communicator.receive_json_from()
        message = {
            "type": "distance_msg",
            "state": "stop",
            "distance": -1,
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_distance_measuring(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application, path="ws/ble-devices/"
        )
        await communicator.connect()
        response = await communicator.receive_json_from()
        message = {
            "type": "distance_msg",
            "state": "scanning",
            "distance": 23.2,
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        test = await DistanceMeasurement.objects.aget(pk=1)
        assert 23.2 == test.distance
        await communicator.disconnect()

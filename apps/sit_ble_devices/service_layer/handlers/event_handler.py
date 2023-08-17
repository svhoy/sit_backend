import json
from channels.layers import get_channel_layer
from apps.sit_ble_devices.service_layer import uow
from sit_ble_devices.domain import events


async def send_connection_info(event: events.WsClientRegisterd):
    send_msg = event.json
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "sit_1", {"type": "send_event", "data": send_msg}
    )


async def send_connection_ping(event: events.WsClientUnregisterd):
    send_msg = json.dumps({"type": "PingWsConnection", "data": {}})
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        event.room_id, {"type": "send_event", "data": send_msg}
    )


async def send_device_list(
    event: events.WsClientRegisterd, uow: uow.UnitOfWork
):
    device_list = []
    async with uow:
        device_list.extend(uow.bleDevices.get_device_list())

    send_msg = {"type": "DeviceList", "data": {"device_list": device_list}}
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "sit_1", {"type": "send_event", "data": json.dumps(send_msg)}
    )


async def send_device_registered(
    event: events.BleDeviceRegistered | events.BleDeviceUnregistered,
):
    send_msg = event.json
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "sit_1", {"type": "send_event", "data": send_msg}
    )


async def redirect_event(
    event: events.BleDeviceConnectError | events.BleDeviceConnectFailed,
):
    data = event.json
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "sit_1", {"type": "send_event", "data": data}
    )


EVENT_HANDLER = {
    events.WsClientRegisterd: [send_connection_info, send_device_list],
    events.WsClientUnregisterd: [send_connection_ping],
    events.BleDeviceRegistered: [send_device_registered],
    events.BleDeviceUnregistered: [send_device_registered],
    events.BleDeviceConnectError: [redirect_event],
    events.BleDeviceConnectFailed: [redirect_event],
}

from channels.layers import get_channel_layer
from sit_ble_devices.domain import commands
from sit_ble_devices.service_layer import uow


async def register_ws_client(
    command: commands.RegisterWsClient, uow: uow.AbstractUnitOfWork
):
    async with uow:
        await uow.wsConnection.add_connection(command.client_id)


async def unregister_ws_client(
    command: commands.UnregisterWsClient, uow: uow.AbstractUnitOfWork
):
    async with uow:
        await uow.wsConnection.remove_connections()


async def register_ble_device(
    command: commands.RegisterBleConnection, uow: uow.UnitOfWork
):
    async with uow:
        await uow.bleDevices.add_connection(command.device_id)


async def unregister_ble_device(
    command: commands.UnregisterWsClient, uow: uow.UnitOfWork
):
    async with uow:
        await uow.bleDevices.remove_connection(command.device_id)


async def save_measurement(command: commands.SaveMesurement):
    pass


async def redirect_command(
    command: commands.ConnectBleDevice
    | commands.DisconnectBleDevice
    | commands.StartDistanceMeasurement
    | commands.StopDistanceMeasurement,
):
    data = command.json
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "sit_1", {"type": "send_command", "data": data}
    )


COMMAND_HANDLER = {
    commands.RegisterWsClient: register_ws_client,
    commands.UnregisterWsClient: unregister_ws_client,
    commands.ConnectBleDevice: redirect_command,
    commands.DisconnectBleDevice: redirect_command,
    commands.RegisterBleConnection: register_ble_device,
    commands.UnregisterBleConnection: unregister_ble_device,
    commands.StartDistanceMeasurement: redirect_command,
    commands.StopDistanceMeasurement: redirect_command,
    commands.SaveMesurement: save_measurement,
}

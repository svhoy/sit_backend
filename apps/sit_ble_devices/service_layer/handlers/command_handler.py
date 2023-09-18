from channels.layers import get_channel_layer
from sit_ble_devices.domain.model import distances
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


async def save_measurement(
    command: commands.SaveMesurement, duow: uow.DistanceUnitOfWork
):
    async with duow:
        measurement = distances.DistanceMeasurement(
            sequence=command.sequence,
            distance=command.distance,
            nlos=command.nlos,
            rssi=command.rssi,
            fpi=command.fpi,
        )
        await duow.distanceMeasurement.add(measurement)
        await duow.commit()


async def save_test_measurement(
    command: commands.SaveTestMeasurement, duow: uow.DistanceUnitOfWork
):
    async with duow:
        measurement = distances.DistanceMeasurement(
            sequence=command.sequence,
            distance=command.distance,
            nlos=command.nlos,
            rssi=command.rssi,
            fpi=command.fpi,
            test_id=command.test_id,
        )
        await duow.distanceMeasurement.add(measurement)
        await duow.commit()


async def redirect_command(
    command: commands.ConnectBleDevice
    | commands.DisconnectBleDevice
    | commands.StartDistanceMeasurement
    | commands.StopDistanceMeasurement
    | commands.StartTestMeasurement,
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
    commands.StartTestMeasurement: redirect_command,
    commands.SaveTestMeasurement: save_test_measurement,
}

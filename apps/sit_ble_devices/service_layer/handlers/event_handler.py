import json

from channels.layers import get_channel_layer
from colorama import deinit
from sit_ble_devices.domain import commands, events
from sit_ble_devices.domain.model import uwbdevice
from sit_ble_devices.service_layer.utils import calibrations

from apps.sit_ble_devices.service_layer import uow


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
        device_list.extend(uow.ble_devices.get_device_list())

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


async def send_calibration_created(event: events.CalibrationCreated):
    send_msg = event.json
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "sit_1", {"type": "send_event", "data": send_msg}
    )


async def send_start_calibration(event: events.CalibrationInitFinished):
    command = commands.StartCalibrationMeasurement(
        calibration_id=event.calibration_id, devices=event.devices
    )
    send_msg = command.json
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "sit_1", {"type": "send_event", "data": send_msg}
    )


async def start_calibration_calc(
    event: events.CalibrationMeasurementFinished,
    cuow: uow.CalibrationUnitOfWork,
):
    result = []
    async with cuow:
        calibration_dom = await cuow.calibration_repo.get_by_id(
            cali_id=event.calibration_id
        )
        result = await calibrations.start_calibration(calibration_dom)
        cuow.calibration_repo.seen.add(calibration_dom)
        calibration_dom.events.append(
            events.CalibrationCalcFinished(
                calibration_id=calibration_dom.calibration_id,
                result=result,
            )
        )


async def finished_calibration(
    event: events.CalibrationCalcFinished, uduow: uow.UwbDeviceUnitOfWork
):
    async with uduow:
        uwbdevice_dom = None
        for device in event.result:
            uwbdevice_dom = await uduow.uwb_device_repo.get_by_id(device[0])
            uwbdevice_dom = await uduow.uwb_device_repo.add_ant_dly(
                uwbdevice_dom,
                uwbdevice.AntDelay(
                    default=False,
                    calibration_id=event.calibration_id,
                    device_id=device[0],
                    tx_ant_delay=device[1],
                    rx_ant_delay=device[2],
                ),
            )
            uduow.uwb_device_repo.seen.add(uwbdevice_dom)
            await uduow.commit()

        uwbdevice_dom.events.append(
            events.CalibrationResultsSaved(calibration_id=event.calibration_id)
        )


async def redirect_event(
    event: events.BleDeviceConnectError
    | events.BleDeviceConnectFailed
    | events.CalibrationMeasurementFinished
    | events.CalibrationCalcFinished
    | events.CalibrationResultsSaved,
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
    events.MeasurementSaved: [redirect_event],
    events.CalibrationCreated: [send_calibration_created],
    events.CalibrationInitFinished: [send_start_calibration],
    events.CalibrationMeasurementFinished: [
        start_calibration_calc,
        redirect_event,
    ],
    events.CalibrationCalcFinished: [finished_calibration, redirect_event],
    events.CalibrationResultsSaved: [redirect_event],
}

# pylint: disable=unused-argument
import logging

from channels.layers import get_channel_layer
from sit_ble_devices.domain import commands
from sit_ble_devices.domain.model import calibration, distances
from sit_ble_devices.service_layer import uow

# create logger
logger = logging.getLogger("service_layer.command_handler")


async def register_ws_client(
    command: commands.RegisterWsClient, uow: uow.UnitOfWork
):
    async with uow:
        await uow.ws_connection.add_connection(command.client_id)


async def unregister_ws_client(
    command: commands.UnregisterWsClient, uow: uow.UnitOfWork
):
    async with uow:
        await uow.ws_connection.remove_connections()


async def register_ble_device(
    command: commands.RegisterBleConnection, uow: uow.UnitOfWork
):
    async with uow:
        await uow.ble_devices.add_connection(command.device_id)


async def unregister_ble_device(
    command: commands.UnregisterBleConnection, uow: uow.UnitOfWork
):
    async with uow:
        await uow.ble_devices.remove_connection(command.device_id)


async def save_measurement(
    command: commands.SaveMesurement, duow: uow.DistanceUnitOfWork
):
    async with duow:
        measurement = distances.DistanceMeasurement(
            initiator_id=command.initiator,
            responder_id=command.responder,
            measurement_type=command.measurement_type,
            sequence=command.sequence,
            measurement=command.measurement,
            distance=command.distance,
            time_round_1=command.time_round_1,
            time_round_2=command.time_round_2,
            time_reply_1=command.time_reply_1,
            time_reply_2=command.time_reply_2,
            nlos_final=command.nlos_final,
            rssi_final=command.rssi_final,
            fpi_final=command.fpi_final,
        )
        await duow.distance_measurement.add(measurement)

        await duow.commit()


async def save_test_measurement(
    command: commands.SaveTestMeasurement, duow: uow.DistanceUnitOfWork
):
    async with duow:
        measurement = distances.DistanceMeasurement(
            initiator_id=command.initiator,
            responder_id=command.responder,
            measurement_type=command.measurement_type,
            sequence=command.sequence,
            measurement=command.measurement,
            distance=command.distance,
            time_round_1=command.time_round_1,
            time_round_2=command.time_round_2,
            time_reply_1=command.time_reply_1,
            time_reply_2=command.time_reply_2,
            nlos_final=command.nlos_final,
            rssi_final=command.rssi_final,
            fpi_final=command.fpi_final,
            test_id=command.test_id,
        )
        await duow.distance_measurement.add(measurement)
        await duow.commit()


async def save_calibration_measurement(
    command: commands.SaveCalibrationMeasurement, duow: uow.DistanceUnitOfWork
):
    async with duow:
        measurement = distances.DistanceMeasurement(
            initiator_id=command.initiator,
            responder_id=command.responder,
            measurement_type=command.measurement_type,
            sequence=command.sequence,
            measurement=command.measurement,
            distance=command.distance,
            time_round_1=command.time_round_1,
            time_round_2=command.time_round_2,
            time_reply_1=command.time_reply_1,
            time_reply_2=command.time_reply_2,
            nlos_final=command.nlos_final,
            rssi_final=command.rssi_final,
            fpi_final=command.fpi_final,
            calibration_id=command.calibration_id,
        )
        await duow.distance_measurement.add(measurement)
        await duow.commit()


async def create_calibration(
    command: commands.CreateCalibration, cuow: uow.CalibrationUnitOfWork
):
    async with cuow:
        new_calibration = calibration.Calibrations(
            calibration_type=command.calibration_type,
            measurement_type=command.measurement_type,
            devices=command.devices,
        )
        await cuow.calibration_repo.add(new_calibration)
        await cuow.commit()


async def add_calibration_distances(
    command: commands.AddCalibrationDistances, cuow: uow.CalibrationUnitOfWork
):
    async with cuow:
        cali_distance_list = []
        calibration_dom = await cuow.calibration_repo.get_by_id(
            cali_id=command.calibration_id
        )
        for cali_distance in command.distance_list:
            new_cali_distance = calibration.CalibrationDistance(
                calibration_id=calibration_dom.calibration_id,
                distance=cali_distance[2],
                initiator_id=cali_distance[0],
                responder_id=cali_distance[1],
            )
            new_cali_distance2 = calibration.CalibrationDistance(
                calibration_id=calibration_dom.calibration_id,
                distance=cali_distance[2],
                initiator_id=cali_distance[1],
                responder_id=cali_distance[0],
            )
            cali_distance_list.append(new_cali_distance)
            cali_distance_list.append(new_cali_distance2)
        await cuow.calibration_repo.add_cali_distances(
            calibration_domain=calibration_dom,
            cali_distances_domains=cali_distance_list,
        )
        await cuow.commit()


async def start_calibration_calc(
    command: commands.StartCalibrationCalc,
    cuow: uow.CalibrationUnitOfWork,
    duow: uow.DistanceUnitOfWork,
):
    logger.info("Starting calibration calculation")


async def redirect_command(
    command: (
        commands.ConnectBleDevice
        | commands.DisconnectBleDevice
        | commands.StartDistanceMeasurement
        | commands.StopDistanceMeasurement
        | commands.StartTestMeasurement
    ),
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
    commands.CreateCalibration: create_calibration,
    commands.AddCalibrationDistances: add_calibration_distances,
    commands.SaveCalibrationMeasurement: save_calibration_measurement,
    commands.StartCalibrationCalc: start_calibration_calc,
}

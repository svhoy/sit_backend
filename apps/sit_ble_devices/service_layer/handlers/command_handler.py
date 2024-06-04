# pylint: disable=unused-argument
import logging

from channels.layers import get_channel_layer
from sit_ble_devices.domain import commands, events
from sit_ble_devices.domain.model import calibration, distances
from sit_ble_devices.service_layer import uow

# create logger
logger = logging.getLogger("sit.service_layer.handler")


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


async def save_simple_calibration_measurement(
    command: commands.SaveSimpleCalibrationMeasurement,
    cmuow: uow.CalibrationMeasurementUnitOfWork,
):
    async with cmuow:
        measurement = distances.CalibrationMeasurements(
            calibration_id=command.calibration_id,
            measurement=command.measurement,
            sequence=command.sequence,
            device_a=command.devices[0],
            device_b=command.devices[1],
            device_c=command.devices[2],
            time_m21=command.time_m21,
            time_m31=command.time_m31,
            time_a21=command.time_a21,
            time_a31=command.time_a31,
            time_b21=command.time_b21,
            time_b31=command.time_b31,
            time_b_i=command.time_tb_i,
            time_b_ii=command.time_tb_ii,
            time_c_i=command.time_tc_i,
            time_c_ii=command.time_tc_ii,
            time_round_1=command.time_round_1,
            time_round_2=command.time_round_2,
            time_reply_1=command.time_reply_1,
            time_reply_2=command.time_reply_2,
            distance=command.distance,
        )
        await cmuow.calibration_measurement.add(measurement)
        await cmuow.commit()


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


async def copie_calibration(
    command: commands.CopieCalibration,
    cuow: uow.CalibrationUnitOfWork,
    duow: uow.DistanceUnitOfWork,
):
    new_calibration_id: int
    async with cuow:
        calibration_dom = await cuow.calibration_repo.get_by_id(
            domain_id=command.copie_calibration_id
        )
        new_calibration = calibration.Calibrations(
            calibration_type=command.calibration_type,
            measurement_type=calibration_dom.measurement_type,
            devices=calibration_dom.devices,
        )
        new_calibration.calibration_id = await cuow.calibration_repo.add(
            new_calibration
        )

        for cali_distance in calibration_dom.cali_distances:
            cali_distance.calibration_id = new_calibration.calibration_id

        await cuow.calibration_repo.add_cali_distances(
            calibration_domain=new_calibration,
            cali_distances_domains=calibration_dom.cali_distances,
            copie=True,
        )
        new_calibration_id = new_calibration.calibration_id

        await cuow.commit()
    async with duow:
        await duow.distance_measurement.update_calibration_id(
            calibration_id=command.copie_calibration_id,
            new_calibration_id=new_calibration_id,
        )
        await duow.commit()

    async with cuow:
        calibration_dom = await cuow.calibration_repo.get_by_id(
            new_calibration_id
        )
        cuow.calibration_repo.seen.add(calibration_dom)
        calibration_dom.events.append(
            events.CalibrationCopied(
                calibration_id=calibration_dom.calibration_id,
                calibration_type=calibration_dom.calibration_type,
            )
        )


async def copie_simple_calibration(
    command: commands.CopieCalibration,
    cuow: uow.CalibrationUnitOfWork,
    cmuow: uow.CalibrationMeasurementUnitOfWork,
):
    new_calibration_id: int
    async with cuow:
        calibration_dom = await cuow.calibration_repo.get_by_id(
            domain_id=command.copie_calibration_id
        )
        new_calibration = calibration.Calibrations(
            calibration_type=command.calibration_type,
            measurement_type=calibration_dom.measurement_type,
            devices=calibration_dom.devices,
        )
        new_calibration.calibration_id = await cuow.calibration_repo.add(
            new_calibration
        )

        for cali_distance in calibration_dom.cali_distances:
            cali_distance.calibration_id = new_calibration.calibration_id

        await cuow.calibration_repo.add_cali_distances(
            calibration_domain=new_calibration,
            cali_distances_domains=calibration_dom.cali_distances,
            copie=True,
        )
        new_calibration_id = new_calibration.calibration_id

        await cuow.commit()
    async with cmuow:
        await cmuow.calibration_measurement.update_calibration_id(
            calibration_id=command.copie_calibration_id,
            new_calibration_id=new_calibration_id,
        )
        await cmuow.commit()

    async with cuow:
        calibration_dom = await cuow.calibration_repo.get_by_id(
            new_calibration_id
        )
        cuow.calibration_repo.seen.add(calibration_dom)
        calibration_dom.events.append(
            events.CalibrationCopied(
                calibration_id=calibration_dom.calibration_id,
                calibration_type=calibration_dom.calibration_type,
            )
        )


async def add_calibration_distances(
    command: commands.AddCalibrationDistances, cuow: uow.CalibrationUnitOfWork
):

    async with cuow:
        cali_distance_list = []

        calibration_dom = await cuow.calibration_repo.get_by_id(
            domain_id=command.calibration_id
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


async def save_measurement_cache(
    command: commands.SaveMeasurementCache,
    duow: uow.DistanceUnitOfWork,
):
    async with duow:
        measurement_list = [
            distances.DistanceMeasurement(
                initiator_id=measurement["initiator"],
                responder_id=measurement["responder"],
                measurement_type=measurement["measurement_type"],
                sequence=measurement["sequence"],
                measurement=measurement["measurement"],
                distance=measurement["distance"],
                time_round_1=measurement["time_round_1"],
                time_round_2=measurement["time_round_2"],
                time_reply_1=measurement["time_reply_1"],
                time_reply_2=measurement["time_reply_2"],
                nlos_final=measurement["nlos"],
                rssi_final=measurement["rssi"],
                fpi_final=measurement["fpi"],
                test_id=measurement["test_id"],
            )
            for measurement in command.measurement_list
        ]
        await duow.distance_measurement.add_bulk(measurement_list)


async def redirect_command(
    command: (
        commands.ConnectBleDevice
        | commands.DisconnectBleDevice
        | commands.StartDistanceMeasurement
        | commands.StopDistanceMeasurement
        | commands.StartTestMeasurement
        | commands.StartDebugCalibration
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
    commands.SaveSimpleCalibrationMeasurement: save_simple_calibration_measurement,
    commands.StartCalibrationCalc: start_calibration_calc,
    commands.CopieCalibration: copie_calibration,
    commands.CopieSimpleCalibration: copie_simple_calibration,
    commands.StartDebugCalibration: redirect_command,
    commands.SaveMeasurementCache: save_measurement_cache,
}

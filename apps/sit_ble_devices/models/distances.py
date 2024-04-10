import logging

from asgiref.sync import sync_to_async
from django.db import models
from sit_ble_devices.domain.model import distances

from .devices import Calibration, UwbDevice
from .tests import DeviceTests

logger = logging.getLogger("sit.domain.model.distance")


class DistanceMeasurement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    test = models.ForeignKey(
        DeviceTests,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="test",
    )
    calibrations = models.ManyToManyField(
        Calibration,
        blank=True,
        related_name="calibrations",
    )
    initiator = models.ForeignKey(
        UwbDevice, related_name="initiator", on_delete=models.DO_NOTHING
    )
    responder = models.ForeignKey(
        UwbDevice, related_name="responder", on_delete=models.DO_NOTHING
    )
    measurement_type = models.CharField(max_length=30)
    sequence = models.IntegerField()
    measurement = models.IntegerField()
    distance = models.FloatField()
    time_round_1 = models.FloatField()
    time_round_2 = models.FloatField()
    time_reply_1 = models.FloatField()
    time_reply_2 = models.FloatField()
    nlos = models.IntegerField(blank=True, null=True)
    recived_signal_strength_index_final = models.FloatField(
        blank=True, null=True
    )
    first_path_index_final = models.FloatField(blank=True, null=True)
    error_distance = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ["created"]

    @staticmethod
    async def from_domain(measurement: distances.DistanceMeasurement):
        test = None
        error_distance = None
        calibration = None
        try:
            if measurement.test_id is not None:
                test = await DeviceTests.objects.aget(id=measurement.test_id)
                if test.real_test_distance is not None:
                    error_distance = (
                        measurement.distance - test.real_test_distance
                    )
                    measurement.edistance = error_distance
            elif measurement.calibration_id is not None:
                calibration = await Calibration.objects.aget(
                    id=measurement.calibration_id
                )
            initiator = await UwbDevice.objects.aget(
                device_id=measurement.initiator_id
            )
            responder = await UwbDevice.objects.aget(
                device_id=measurement.responder_id
            )
            distance_model = await DistanceMeasurement.objects.acreate(
                initiator=initiator,
                responder=responder,
                measurement_type=measurement.measurement_type,
                sequence=measurement.sequence,
                measurement=measurement.measurement,
                distance=measurement.distance,
                time_round_1=measurement.time_round_1,
                time_round_2=measurement.time_round_2,
                time_reply_1=measurement.time_reply_1,
                time_reply_2=measurement.time_reply_2,
                nlos=measurement.nlos_final,
                recived_signal_strength_index_final=measurement.rssi_final,
                first_path_index_final=measurement.fpi_final,
                error_distance=error_distance,
                test=test,
            )
        except Exception as e:
            logger.error(f"Error creating distance measurement: {e}")
        try:
            if calibration is not None:
                await sync_to_async(distance_model.calibrations.add)(
                    calibration
                )
        except Exception as e:
            logger.error(f"Error Appending calibration to distance: {e}")
        await distance_model.asave()

    @staticmethod
    async def update_from_domain(measurement: distances.DistanceMeasurement):
        if measurement.test_id is not None:
            test = await DeviceTests.objects.aget(id=measurement.test_id)
            if test.real_test_distance is not None:
                error_distance = measurement.distance - test.real_test_distance
                measurement.edistance = error_distance
        elif measurement.calibration_id is not None:
            calibration = await Calibration.objects.aget(
                id=measurement.calibration_id
            )
        try:
            try:
                distance_model = await DistanceMeasurement.objects.aget(
                    id=measurement.measurement_id
                )
            except DistanceMeasurement.DoesNotExist:
                distance_model = await DistanceMeasurement()
        except Exception as e:
            logger.error(f"Error updating distance: {e}")

        distance_model.initiator = await UwbDevice.objects.aget(
            device_id=measurement.initiator_id
        )
        distance_model.responder = await UwbDevice.objects.aget(
            device_id=measurement.responder_id
        )
        distance_model.measurement_type = measurement.measurement_type
        distance_model.sequence = measurement.sequence
        distance_model.measurement = measurement.measurement
        distance_model.distance = measurement.distance
        distance_model.time_round_1 = measurement.time_round_1
        distance_model.time_round_2 = measurement.time_round_2
        distance_model.time_reply_1 = measurement.time_reply_1
        distance_model.time_reply_2 = measurement.time_reply_2
        distance_model.nlos = measurement.nlos_final
        distance_model.recived_signal_strength_index_final = (
            measurement.rssi_final
        )
        distance_model.first_path_index_final = measurement.fpi_final
        distance_model.error_distance = measurement.edistance

        try:
            if calibration is not None:
                await sync_to_async(distance_model.calibrations.add)(
                    calibration
                )
        except Exception as e:
            print(f"Error Appending calibration to distance: {e}")

        await distance_model.asave()

    def to_domain(self) -> distances.DistanceMeasurement:
        d = distances.DistanceMeasurement(
            measurement_id=self.id,
            initiator_id=self.initiator.device_id,
            responder_id=self.responder.device_id,
            sequence=self.sequence,
            measurement_type=self.measurement_type,
            measurement=self.measurement,
            distance=self.distance,
            time_round_1=self.time_round_1,
            time_round_2=self.time_round_2,
            time_reply_1=self.time_reply_1,
            time_reply_2=self.time_reply_2,
            nlos_final=self.nlos,
            rssi_final=self.recived_signal_strength_index_final,
            fpi_final=self.first_path_index_final,
            edistance=self.error_distance,
        )
        return d

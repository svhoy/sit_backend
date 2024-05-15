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
        calibration = None
        if measurement.test_id is not None:
            test = await DeviceTests.objects.aget(id=measurement.test_id)
            if test.real_test_distance is not None:
                error_distance = measurement.distance - test.real_test_distance
                measurement.edistance = error_distance
        elif (
            measurement.calibration_id is not None
            and len(measurement.calibration_id) > 0
        ):
            calibration = await Calibration.objects.aget(
                id=measurement.calibration_id
            )
        try:
            try:
                distance_model = await DistanceMeasurement.objects.aget(
                    id=measurement.measurement_id
                )
            except DistanceMeasurement.DoesNotExist:
                distance_model = DistanceMeasurement()
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
        distance_model.test = test
        await distance_model.asave()
        try:
            if calibration is not None:
                await sync_to_async(distance_model.calibrations.add)(
                    calibration
                )
        except Exception as e:
            print(f"Error Appending calibration to distance: {e}")

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


class CalibrationMeasurements(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    calibrations = models.ManyToManyField(
        Calibration,
        blank=True,
        related_name="calibration",
    )
    device_a = models.ForeignKey(
        UwbDevice,
        related_name="device_a",
        on_delete=models.DO_NOTHING,
    )
    device_b = models.ForeignKey(
        UwbDevice,
        related_name="device_b",
        on_delete=models.DO_NOTHING,
    )
    device_c = models.ForeignKey(
        UwbDevice,
        related_name="device_c",
        on_delete=models.DO_NOTHING,
    )
    sequence = models.IntegerField()
    measurement = models.IntegerField()
    time_m21 = models.FloatField(default=0.0)
    time_m31 = models.FloatField(default=0.0)
    time_a21 = models.FloatField(default=0.0)
    time_a31 = models.FloatField(default=0.0)
    time_b21 = models.FloatField(default=0.0)
    time_b31 = models.FloatField(default=0.0)
    time_b_i = models.FloatField(default=0.0)
    time_b_ii = models.FloatField(default=0.0)
    time_c_i = models.FloatField(default=0.0)
    time_c_ii = models.FloatField(default=0.0)
    time_round_1 = models.FloatField(default=0.0)
    time_round_2 = models.FloatField(default=0.0)
    time_reply_1 = models.FloatField(default=0.0)
    time_reply_2 = models.FloatField(default=0.0)
    distance = models.FloatField(default=0.0)

    class Meta:
        ordering = ["created"]

    @staticmethod
    async def update_from_domain(
        measurement: distances.CalibrationMeasurements,
    ):
        calibration = await Calibration.objects.aget(
            id=measurement.calibration_id
        )
        try:
            measurement_model = await CalibrationMeasurements.objects.aget(
                id=measurement.measurement_id
            )
        except CalibrationMeasurements.DoesNotExist:
            measurement_model = CalibrationMeasurements()

        try:
            measurement_model.device_a = await UwbDevice.objects.aget(
                device_id=measurement.device_a
            )
            measurement_model.device_b = await UwbDevice.objects.aget(
                device_id=measurement.device_b
            )
            measurement_model.device_c = await UwbDevice.objects.aget(
                device_id=measurement.device_c
            )
        except Exception as e:
            logger.error(f"Error updating measurement: {e}")

        measurement_model.sequence = measurement.sequence
        measurement_model.measurement = measurement.measurement
        measurement_model.time_m21 = measurement.time_m21
        measurement_model.time_m31 = measurement.time_m31
        measurement_model.time_a21 = measurement.time_a21
        measurement_model.time_a31 = measurement.time_a31
        measurement_model.time_b21 = measurement.time_b21
        measurement_model.time_b31 = measurement.time_b31
        measurement_model.time_b_i = measurement.time_b_i
        measurement_model.time_b_ii = measurement.time_b_ii
        measurement_model.time_c_i = measurement.time_c_i
        measurement_model.time_c_ii = measurement.time_c_ii
        measurement_model.time_round_1 = measurement.time_round_1
        measurement_model.time_round_2 = measurement.time_round_2
        measurement_model.time_reply_1 = measurement.time_reply_1
        measurement_model.time_reply_2 = measurement.time_reply_2
        measurement_model.distance = measurement.distance

        try:
            await measurement_model.asave()
        except Exception as e:
            logger.error(f"Error updating measurement: {e}")
        try:
            if calibration is not None:
                await sync_to_async(measurement_model.calibrations.add)(
                    calibration
                )
        except Exception as e:
            print(f"Error Appending calibration to distance: {e}")

    def to_domain(self) -> distances.CalibrationMeasurements:
        d = distances.CalibrationMeasurements(
            measurement_id=self.id,
            device_a=self.device_a.device_id,
            device_b=self.device_b.device_id,
            device_c=self.device_c.device_id,
            sequence=self.sequence,
            measurement=self.measurement,
            time_b_i=self.time_b_i,
            time_b_ii=self.time_b_ii,
            time_c_i=self.time_c_i,
            time_c_ii=self.time_c_ii,
            time_m21=self.time_m21,
            time_m31=self.time_m31,
            time_a21=self.time_a21,
            time_a31=self.time_a31,
            time_b21=self.time_b21,
            time_b31=self.time_b31,
            time_round_1=self.time_round_1,
            time_round_2=self.time_round_2,
            time_reply_1=self.time_reply_1,
            time_reply_2=self.time_reply_2,
            distance=self.distance,
        )
        return d

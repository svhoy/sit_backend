from django.db import models
from sit_ble_devices.domain.model import distances

from .devices import Calibration, UwbDevice
from .tests import DeviceTests


class DistanceMeasurement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    test = models.ForeignKey(
        DeviceTests,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="test",
    )
    calibration = models.ForeignKey(
        Calibration,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="calibration",
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
        if measurement.test_id is not None:
            test = await DeviceTests.objects.aget(id=measurement.test_id)
            if test.real_test_distance is not None:
                error_distance = measurement.distance - test.real_test_distance
                measurement.edistance = error_distance
        elif measurement.claibration_id is not None:
            calibration = await Calibration.objects.aget(
                id=measurement.claibration_id
            )
        initiator = await UwbDevice.objects.aget(
            device_id=measurement.initiator
        )
        responder = await UwbDevice.objects.aget(
            device_id=measurement.responder
        )
        distance_model = await DistanceMeasurement.objects.acreate(
            initiator=initiator_id,
            responder=responder_id,
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
            calibration=calibration,
        )
        await distance_model.asave()

    def to_domain(self) -> distances.DistanceMeasurement:
        d = distances.DistanceMeasurement(
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

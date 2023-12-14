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
    sequence = models.IntegerField()
    measurement = models.IntegerField()
    distance = models.FloatField()
    nlos = models.IntegerField(blank=True, null=True)
    RecivedSignalStrengthIndex = models.FloatField(blank=True, null=True)
    firstPathIndex = models.FloatField(blank=True, null=True)
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
            initiator=initiator,
            responder=responder,
            sequence=measurement.sequence,
            measurement=measurement.measurement,
            distance=measurement.distance,
            nlos=measurement.nlos,
            RecivedSignalStrengthIndex=measurement.rssi,
            firstPathIndex=measurement.fpi,
            error_distance=error_distance,
            test=test,
            calibration=calibration,
        )
        await distance_model.asave()

    def to_domain(self) -> distances.DistanceMeasurement:
        d = distances.DistanceMeasurement(
            initiator=self.initiator,
            responder=self.responder,
            sequence=self.sequence,
            measurement=self.measurement,
            distance=self.distance,
            nlos=self.nlos,
            rssi=self.RecivedSignalStrengthIndex,
            fpi=self.firstPathIndex,
            edistance=self.error_distance,
        )
        return d

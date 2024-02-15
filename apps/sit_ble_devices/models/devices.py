from asgiref.sync import sync_to_async
from django.db import models
from sit_ble_devices.domain.model import calibration, uwbdevice


class UwbDevice(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    device_name = models.CharField(max_length=30)
    device_id = models.CharField(max_length=20, unique=True)
    comments = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ["created"]

    @staticmethod
    async def from_domain(uwbdevice_dom: uwbdevice.UwbDevice):
        device = await UwbDevice.objects.acreate(
            device_name=uwbdevice_dom.device_name,
            device_id=uwbdevice_dom.device_id,
            comments=uwbdevice_dom.comments,
        )
        await device.asave()

    async def to_domain(self) -> uwbdevice.UwbDevice:
        d = uwbdevice.UwbDevice(
            device_id=self.device_id,
            device_name=self.device_name,
            comments=self.comments,
        )
        return d


class Calibration(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=30)
    measurement_type = models.CharField(max_length=30)
    temperature = models.IntegerField(blank=True, null=True)
    iterations = models.IntegerField(default=100)
    devices = models.ManyToManyField(UwbDevice, blank=True)
    comments = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ["created"]

    @staticmethod
    async def from_domain(calibration_dom: calibration.Calibrations) -> int:
        distance_model = await Calibration.objects.acreate(
            type=calibration_dom.calibration_type,
        )
        devices = []
        for device in calibration_dom.devices:
            device_model = await UwbDevice.objects.aget(device_id=device)
            devices.append(device_model)

        await distance_model.devices.aset(devices)
        await distance_model.asave()
        return distance_model.id

    async def to_domain(self) -> calibration.Calibrations:
        devices_queryset = self.devices.all()
        device_list = await sync_to_async(list)(
            devices_queryset.values_list("device_id", flat=True)
        )
        d = calibration.Calibrations(
            calibration_id=self.id,
            calibration_type=self.type,
            devices=device_list,
        )
        return d


class CalibrationsDistances(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    calibration_mod = models.ForeignKey(Calibration, on_delete=models.CASCADE)
    distance = models.FloatField()
    initiator = models.ForeignKey(
        UwbDevice,
        related_name="cali_initiator_device",
        on_delete=models.DO_NOTHING,
    )
    responder = models.ForeignKey(
        UwbDevice,
        related_name="cali_responder_device",
        on_delete=models.DO_NOTHING,
    )

    @staticmethod
    async def from_domain(
        cali_distance_dom: calibration.CalibrationDistance,
    ) -> int:
        calibration_mod = await Calibration.objects.aget(
            id=cali_distance_dom.calibration_id
        )
        initiator_mod = await UwbDevice.objects.aget(
            device_id=cali_distance_dom.initiator_device_id
        )
        responder_mod = await UwbDevice.objects.aget(
            device_id=cali_distance_dom.responder_device_id
        )
        model = await CalibrationsDistances.objects.acreate(
            calibration_mod=calibration_mod,
            distance=cali_distance_dom.distance,
            initiator=initiator_mod,
            responder=responder_mod,
        )
        await model.asave()
        return model.id

    def to_domain(self) -> calibration.CalibrationDistance:
        d = calibration.CalibrationDistance(
            distance_id=self.id,
            calibration_id=self.calibration_mod.id,
            distance=self.distance,
            initiator_id=self.initiator.id,
            responder_id=self.responder.id,
        )
        return d


class AntDelay(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=False)
    calibration_mod = models.ForeignKey(Calibration, on_delete=models.CASCADE)
    device = models.ForeignKey(UwbDevice, on_delete=models.CASCADE)
    tx_ant_delay = models.FloatField(default=513.0e-16)
    rx_ant_delay = models.FloatField(default=513.0e-16)

    @staticmethod
    async def from_domain(ant_dly_dom: uwbdevice.AntDelay) -> int:
        calibration_mod = await Calibration.objects.aget(
            id=ant_dly_dom.calibration_id
        )
        device = await UwbDevice.objects.aget(device_id=ant_dly_dom.device_id)
        ant_dly_mod = await AntDelay.objects.acreate(
            default=ant_dly_dom.default,
            calibration_mod=calibration_mod,
            device=device,
            tx_ant_delay=ant_dly_dom.tx_ant_delay,
            rx_ant_delay=ant_dly_dom.rx_ant_delay,
        )
        await ant_dly_mod.asave()
        return ant_dly_mod.id

    async def to_domain(self) -> uwbdevice.AntDelay:
        d = uwbdevice.AntDelay(
            ant_delay_id=self.id,
            calibration_id=self.calibration_mod.id,
            default=self.default,
            device_id=self.device.device_id,
            tx_ant_delay=self.tx_ant_delay,
            rx_ant_delay=self.rx_ant_delay,
        )
        return d

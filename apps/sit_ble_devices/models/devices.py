from django.db import models


class Calibration(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=30)
    temperature = models.IntegerField(blank=True)
    iterations = models.IntegerField(default=100)
    comments = models.CharField(max_length=300, blank=True)


class UwbDevice(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    device_name = models.CharField(max_length=30)
    device_id = models.CharField(max_length=20, unique=True)
    comments = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ["created"]


class CalibrationsDistances(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    calibration = models.ForeignKey(Calibration, on_delete=models.CASCADE)
    distance = models.FloatField()
    initiator = models.ForeignKey(
        UwbDevice, related_name="initiator", on_delete=models.DO_NOTHING
    )
    responder = models.ForeignKey(
        UwbDevice, related_name="responder", on_delete=models.DO_NOTHING
    )


class AntDelay(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=True)
    calibration = models.ForeignKey(Calibration, on_delete=models.CASCADE)
    device = models.ForeignKey(UwbDevice, on_delete=models.CASCADE)
    tx_ant_delay = models.IntegerField(default=16385)
    rx_ant_delay = models.IntegerField(default=16385)

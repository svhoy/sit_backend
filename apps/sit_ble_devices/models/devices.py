from django.db import models


class Calibration(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=True)
    tx_ant_delay = models.IntegerField(default=16385)
    rx_ant_delay = models.IntegerField(default=16385)
    temperature = models.IntegerField()


class UwbDevice(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    device_name = models.CharField(max_length=30)
    device_id = models.CharField(max_length=20, unique=True)
    ant_calibraition = models.ManyToManyField(Calibration, blank=True)
    comments = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ["created"]

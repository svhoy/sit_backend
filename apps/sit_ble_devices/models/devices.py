from django.db import models


class UwbDevice(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    device_name = models.CharField(max_length=30)
    device_id = models.CharField(max_length=15, unique=True)
    comments = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ["created"]

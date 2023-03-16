from django.db import models


# Create your models here.
class DistanceMeasurement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    distance = models.FloatField()

    class Meta:
        ordering = ["created"]

from django.db import models


class MeasurementTestSettings(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING)
    test_name = models.CharField(max_length=100, unique=True)
    test_type = models.CharField(max_length=30)
    test_min_measurements = models.IntegerField(null=True, blank=True)
    test_max_measurements = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["created"]


class MeasurementTest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING)
    test_settings = models.OneToOneField(
        MeasurementTestSettings,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["created"]


class DistanceMeasurement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    distance = models.FloatField()
    test = models.ForeignKey(
        MeasurementTest, null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["created"]

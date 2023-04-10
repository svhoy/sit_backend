from django.core.validators import MinValueValidator
from django.db import models


class DeviceTestGroups(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING)
    test_name = models.CharField(max_length=100, unique=True)
    test_description = models.CharField(max_length=300, blank=True, null=True)
    test_type = models.CharField(max_length=30)
    test_distance = models.FloatField(
        validators=[MinValueValidator(0.0)], null=True, blank=True
    )
    test_unit = models.CharField(
        default="m", max_length=3, null=True, blank=True
    )
    test_min_measurements = models.PositiveIntegerField(null=True, blank=True)
    test_max_measurements = models.PositiveIntegerField(null=True, blank=True)

    comments = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ["created"]


class DeviceTests(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING)
    test_group = models.ForeignKey(
        DeviceTestGroups,
        on_delete=models.CASCADE,
    )
    real_test_distance = models.FloatField(
        validators=[MinValueValidator(0.0)], null=True, blank=True
    )
    comments = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ["created"]


class DistanceMeasurement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    distance = models.FloatField()

    test = models.ForeignKey(
        DeviceTests,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="test",
    )

    class Meta:
        ordering = ["created"]

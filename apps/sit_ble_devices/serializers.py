from rest_framework import serializers

from .models import (
    DistanceMeasurement,
    MeasurementTest,
    MeasurementTestSettings,
)


class DistanceMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceMeasurement
        fields = "__all__"


class MeasurementTestSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementTestSettings
        fields = "__all__"


class MeasurementTestSerializer(serializers.ModelSerializer):
    test_settings = MeasurementTestSettingsSerializer(read_only=True)

    class Meta:
        model = MeasurementTest
        fields = "__all__"

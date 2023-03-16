from rest_framework import serializers

from .models import DistanceMeasurement


class DistanceMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceMeasurement
        fields = "__all__"

from rest_framework import serializers

from .models import DeviceTestGroups, DeviceTests, DistanceMeasurement


class DistanceMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceMeasurement
        fields = "__all__"


class DeviceTestGroupsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = DeviceTestGroups
        fields = "__all__"


class DeviceTestsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="owner.username")
    test_group_name = serializers.ReadOnlyField(source="test_group.test_name")

    class Meta:
        model = DeviceTests
        fields = "__all__"

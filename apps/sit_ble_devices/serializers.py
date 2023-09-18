from rest_framework import serializers

from .models import (
    DeviceTestGroups,
    DeviceTests,
    DistanceMeasurement,
    UwbDevice,
)


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
    initiator_device_name = serializers.ReadOnlyField(
        source="initiator_device.device_name"
    )
    initiator_device_id = serializers.ReadOnlyField(
        source="initiator_device.device_id"
    )
    responder_device_name = serializers.ReadOnlyField(
        source="responder_device.device_name"
    )
    responder_device_id = serializers.ReadOnlyField(
        source="responder_device.device_id"
    )

    class Meta:
        model = DeviceTests
        fields = "__all__"


class UwbDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UwbDevice
        fields = "__all__"

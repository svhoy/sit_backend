from numpy import source
from rest_framework import serializers

from .models import (
    AntDelay,
    Calibration,
    CalibrationsDistances,
    DeviceTestGroups,
    DeviceTests,
    DistanceMeasurement,
    UwbDevice,
)


class CalibrationsDistancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibrationsDistances
        fields = "__all__"


class CalibrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calibration
        fields = "__all__"


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

    antenna_delay_init_tx = serializers.ReadOnlyField(
        source="antenna_delay_initator.tx_ant_delay"
    )

    antenna_delay_init_rx = serializers.ReadOnlyField(
        source="antenna_delay_initator.rx_ant_delay"
    )

    antenna_delay_resp_tx = serializers.ReadOnlyField(
        source="antenna_delay_responder.tx_ant_delay"
    )

    antenna_delay_resp_rx = serializers.ReadOnlyField(
        source="antenna_delay_responder.rx_ant_delay"
    )

    class Meta:
        model = DeviceTests
        fields = "__all__"


class UwbDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UwbDevice
        fields = "__all__"


class AntDelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = AntDelay
        fields = "__all__"

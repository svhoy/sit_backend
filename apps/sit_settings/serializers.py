# Third Party
from rest_framework import serializers

from .models import UwbDeviceSettings


class UwbDeviceSettingsSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    url = serializers.HyperlinkedIdentityField(
        view_name="sit_settings:uwbdevicesettings-detail",
    )

    class Meta:
        model = UwbDeviceSettings
        fields = [
            "url",
            "id",
            "name",
            "owner",
            "channel_num",
            "premable_length_tx",
            "preamble_chunk_size",
            "tx_preamble_code",
            "rx_preamble_code",
            "sfd_mode",
            "data_rate",
            "phy_header_mode",
            "phy_rate",
            "pulse_rep_freq",
            "sfd_timeout",
            "sts_mode",
            "sts_length",
            "pdoa_mode",
        ]

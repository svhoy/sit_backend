# Third Party
from django.db import models


# Create your models here.

CHANNEL_NUM_CHOICES = [
    (5, 5),
    (9, 9),
]

PULSE_REP_FREQ_CHOICES = [
    ("DWT_PRF_16M", "DWT_PRF_16M"),
    ("DWT_PRF_64M", "DWT_PRF_64M"),
    ("DWT_PRF_SCP", "DWT_PRF_SCP"),
]

PREMABLE_LENGTH_TX = [
    ("DWT_PLEN_4096", "DWT_PLEN_4096"),
    ("DWT_PLEN_2048", "DWT_PLEN_2048"),
    ("DWT_PLEN_1536", "DWT_PLEN_1536"),
    ("DWT_PLEN_1024", "DWT_PLEN_1024"),
    ("DWT_PLEN_512", "DWT_PLEN_512"),
    ("DWT_PLEN_256", "DWT_PLEN_256"),
    ("DWT_PLEN_128", "DWT_PLEN_128"),
    ("DWT_PLEN_64", "DWT_PLEN_64"),
    ("DWT_PLEN_32", "DWT_PLEN_32"),
    ("DWT_PLEN_72", "DWT_PLEN_72"),
]

PREAMBLE_CHUNK_SIZE = [
    ("DWT_PAC8", "DWT_PAC8"),
    ("DWT_PAC16", "DWT_PAC16"),
    ("DWT_PAC32", "DWT_PAC32"),
    ("DWT_PAC64", "DWT_PAC64"),
]

DATA_RATE = [
    ("DWT_BR_850K", "DWT_BR_850K"),
    ("DWT_BR_6M8", "DWT_BR_6M8"),
    ("DWT_BR_NODATA", "DWT_BR_NODATA"),
]

SFD_FIELD = [
    ("DWT_SFD_IEEE_4A", "DWT_SFD_IEEE_4A"),
    ("DWT_SFD_DW_8", "DWT_SFD_DW_8"),
    ("DWT_SFD_DW_16", "DWT_SFD_DW_16"),
    ("DWT_SFD_IEEE_4Z", "DWT_SFD_IEEE_4Z"),
    ("DWT_SFD_LEN8", "DWT_SFD_LEN8"),
    ("DWT_SFD_LEN16", "DWT_SFD_LEN16"),
]

PHY_HEADER_MODE = [
    ("DWT_PHRMODE_STD", "DWT_PHRMODE_STD"),
    ("DWT_PHRMODE_EXT", "DWT_PHRMODE_EXT"),
]

PHR_RATE = [
    ("DWT_PHRRATE_STD", "DWT_PHRRATE_STD"),
    ("DWT_PHRRATE_DTA", "DWT_PHRRATE_DTA"),
]

STS_MODE = [
    ("DWT_STS_MODE_OFF", "DWT_STS_MODE_OFF"),
    ("DWT_STS_MODE_1", "DWT_STS_MODE_1"),
    ("DWT_STS_MODE_2", "DWT_STS_MODE_2"),
    ("DWT_STS_MODE_ND", "DWT_STS_MODE_ND"),
    ("DWT_STS_MODE_SDC", "DWT_STS_MODE_SDC"),
    ("DWT_STS_MODE_MASK", "DWT_STS_MODE_MASK"),
    ("DWT_STS_MODE_MASK_NO_SDC", "DWT_STS_MODE_MASK_NO_SDC"),
]

STS_LENGTH = [
    ("DWT_STS_LEN_32", "DWT_STS_LEN_32"),
    ("DWT_STS_LEN_64", "DWT_STS_LEN_64"),
    ("DWT_STS_LEN_128", "DWT_STS_LEN_128"),
    ("DWT_STS_LEN_256", "DWT_STS_LEN_256"),
    ("DWT_STS_LEN_512", "DWT_STS_LEN_512"),
]

PDOA_MODE = [
    ("DWT_PDOA_M0", "DWT_PDOA_M0"),
    ("DWT_PDOA_M1", "DWT_PDOA_M1"),
    ("DWT_PDOA_M3", "DWT_PDOA_M3"),
]


class UwbDeviceSettings(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        "auth.User", related_name="settings", on_delete=models.CASCADE
    )
    channel_num = models.IntegerField(choices=CHANNEL_NUM_CHOICES, default=5)
    premable_length_tx = models.CharField(
        choices=PREMABLE_LENGTH_TX, default="DWT_PLEN_2048", max_length=15
    )
    preamble_chunk_size = models.CharField(
        choices=PREAMBLE_CHUNK_SIZE, default="DWT_PAC8", max_length=15
    )
    tx_preamble_code = models.IntegerField(default=10)
    rx_preamble_code = models.IntegerField(default=10)
    sfd_mode = models.CharField(
        default="DWT_SFD_DW_8", choices=SFD_FIELD, max_length=15
    )
    data_rate = models.CharField(
        choices=DATA_RATE, default="DWT_BR_6M8", max_length=15
    )
    phy_header_mode = models.CharField(
        choices=PHY_HEADER_MODE, default="DWT_PHRMODE_STD", max_length=15
    )
    phy_rate = models.CharField(
        choices=PHR_RATE, default="DWT_PHRRATE_STD", max_length=15
    )
    pulse_rep_freq = models.CharField(
        choices=PULSE_REP_FREQ_CHOICES, default="DWT_PRF_64M", max_length=15
    )
    # SFD timeout (preamble length + 1 + SFD length - PAC size).
    # Used in RX only.
    sfd_timeout = models.IntegerField(default=129)
    sts_mode = models.CharField(
        choices=STS_MODE, default="DWT_STS_MODE_OFF", max_length=24
    )
    sts_length = models.CharField(
        choices=STS_LENGTH, default="DWT_STS_LEN_32", max_length=15
    )
    pdoa_mode = models.CharField(
        choices=PDOA_MODE, default="DWT_PDOA_M0", max_length=15
    )

    class Meta:
        ordering = ["created"]


class TestSettings(models.Model):
    pass

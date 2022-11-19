# Generated by Django 4.1 on 2022-10-25 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sit_settings", "0002_uwbdevicesettings_data_rate_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="uwbdevicesettings",
            name="pdoa_mode",
            field=models.CharField(
                choices=[
                    ("DWT_PDOA_M0", "DWT_PDOA_M0"),
                    ("DWT_PDOA_M1", "DWT_PDOA_M1"),
                    ("DWT_PDOA_M3", "DWT_PDOA_M3"),
                ],
                default="DWT_PDOA_OFF",
                max_length=15,
            ),
        ),
        migrations.AddField(
            model_name="uwbdevicesettings",
            name="phy_rate",
            field=models.CharField(
                choices=[
                    ("DWT_PHRRATE_STD", "DWT_PHRRATE_STD"),
                    ("DWT_PHRRATE_DTA", "DWT_PHRRATE_DTA"),
                ],
                default="DWT_PHRRATE_STD",
                max_length=15,
            ),
        ),
        migrations.AddField(
            model_name="uwbdevicesettings",
            name="sts_length",
            field=models.CharField(
                choices=[
                    ("DWT_STS_LEN_32", "DWT_STS_LEN_32"),
                    ("DWT_STS_LEN_64", "DWT_STS_LEN_64"),
                    ("DWT_STS_LEN_128", "DWT_STS_LEN_128"),
                    ("DWT_STS_LEN_256", "DWT_STS_LEN_256"),
                    ("DWT_STS_LEN_512", "DWT_STS_LEN_512"),
                ],
                default="DWT_STS_LEN_32",
                max_length=15,
            ),
        ),
        migrations.AddField(
            model_name="uwbdevicesettings",
            name="sts_mode",
            field=models.CharField(
                choices=[
                    ("DWT_STS_MODE_OFF", "DWT_STS_MODE_OFF"),
                    ("DWT_STS_MODE_1", "DWT_STS_MODE_1"),
                    ("DWT_STS_MODE_2", "DWT_STS_MODE_2"),
                    ("DWT_STS_MODE_ND", "DWT_STS_MODE_ND"),
                    ("DWT_STS_MODE_SDC", "DWT_STS_MODE_SDC"),
                    ("DWT_STS_MODE_MASK", "DWT_STS_MODE_MASK"),
                    ("DWT_STS_MODE_MASK_NO_SDC", "DWT_STS_MODE_MASK_NO_SDC"),
                ],
                default="DWT_STS_MODE_OFF",
                max_length=24,
            ),
        ),
    ]

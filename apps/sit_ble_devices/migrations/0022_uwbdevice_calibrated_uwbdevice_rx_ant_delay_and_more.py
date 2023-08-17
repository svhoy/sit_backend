# Generated by Django 4.2.1 on 2023-07-16 16:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sit_ble_devices", "0021_devicetests_initiator_device_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="uwbdevice",
            name="calibrated",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="uwbdevice",
            name="rx_ant_delay",
            field=models.IntegerField(default=16385),
        ),
        migrations.AddField(
            model_name="uwbdevice",
            name="tx_ant_delay",
            field=models.IntegerField(default=16385),
        ),
    ]

# Generated by Django 4.2.1 on 2023-07-05 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("sit_ble_devices", "0020_alter_uwbdevice_device_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="devicetests",
            name="initiator_device",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="initiator_device",
                to="sit_ble_devices.uwbdevice",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="devicetests",
            name="responder_device",
            field=models.ForeignKey(
                default=3,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="responder_device",
                to="sit_ble_devices.uwbdevice",
            ),
            preserve_default=False,
        ),
    ]

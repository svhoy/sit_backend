# Generated by Django 5.0.1 on 2024-04-01 15:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sit_ble_devices", "0038_calibration_calibration_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="distancemeasurement",
            name="calibration",
            field=models.ManyToManyField(
                blank=True,
                related_name="calibration",
                to="sit_ble_devices.calibration",
            ),
        ),
    ]

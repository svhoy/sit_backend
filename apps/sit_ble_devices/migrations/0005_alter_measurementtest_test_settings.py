# Generated by Django 4.1.7 on 2023-03-28 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "sit_ble_devices",
            "0004_measurementtestsettings_measurementtest_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="measurementtest",
            name="test_settings",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="sit_ble_devices.measurementtestsettings",
            ),
        ),
    ]

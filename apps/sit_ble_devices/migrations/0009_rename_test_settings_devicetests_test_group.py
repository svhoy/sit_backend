# Generated by Django 4.1.7 on 2023-03-31 22:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "sit_ble_devices",
            "0008_rename_measurementtestsettings_devicetestgroups_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="devicetests",
            old_name="test_settings",
            new_name="test_group",
        ),
    ]

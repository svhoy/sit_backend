# Generated by Django 4.2.1 on 2023-06-27 17:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sit_ble_devices", "0019_alter_uwbdevice_device_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uwbdevice",
            name="device_id",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
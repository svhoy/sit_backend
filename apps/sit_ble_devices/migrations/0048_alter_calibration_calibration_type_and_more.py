# Generated by Django 5.0.1 on 2024-05-15 17:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sit_ble_devices", "0047_calibrationmeasurements_distance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="calibration",
            name="calibration_type",
            field=models.CharField(
                choices=[
                    (
                        "Antenna Calibration (ASP014)",
                        "Antenna Calibration (ASP014)",
                    ),
                    (
                        "Antenna Calibration (ASP014) - SSTWR",
                        "Antenna Calibration (ASP014) - SSTWR",
                    ),
                    (
                        "Antenna Calibration (ASP014) - DSTWR",
                        "Antenna Calibration (ASP014) - DSTWR",
                    ),
                    (
                        "Antenna Calibration (PSO) - EDM SSTWR",
                        "Antenna Calibration (PSO) - EDM SSTWR",
                    ),
                    (
                        "Antenna Calibration (PSO) - EDM DSTWR",
                        "Antenna Calibration (PSO) - EDM DSTWR",
                    ),
                    (
                        "Antenna Calibration (PSO) - EDM",
                        "Antenna Calibration (PSO) - EDM",
                    ),
                    (
                        "Antenna Calibration (PSO) - SSTWR",
                        "Antenna Calibration (PSO) - SSTWR",
                    ),
                    (
                        "Antenna Calibration (PSO) - SDS",
                        "Antenna Calibration (PSO) - SDS",
                    ),
                    (
                        "Antenna Calibration (PSO) - SDS",
                        "Antenna Calibration (PSO) - SDS",
                    ),
                    (
                        "Antenna Calibration (GNA) - ADS",
                        "Antenna Calibration (GNA) - ADS",
                    ),
                    (
                        "Antenna Calibration (GNA) - ADS",
                        "Antenna Calibration (GNA) - ADS",
                    ),
                    (
                        "Antenna Calibration (GNA) - ADS",
                        "Antenna Calibration (GNA) - ADS",
                    ),
                    (
                        "Antenna Calibration (Simple)",
                        "Antenna Calibration (Simple)",
                    ),
                    (
                        "Antenna Calibration (Extended)",
                        "Antenna Calibration (Extended)",
                    ),
                    (
                        "Antenna Calibration (Two Device)",
                        "Antenna Calibration (Two Device)",
                    ),
                ],
                max_length=40,
            ),
        ),
        migrations.AlterField(
            model_name="calibrationmeasurements",
            name="time_a21",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="calibrationmeasurements",
            name="time_a31",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="calibrationmeasurements",
            name="time_b21",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="calibrationmeasurements",
            name="time_b31",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="calibrationmeasurements",
            name="time_b_i",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="calibrationmeasurements",
            name="time_b_ii",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="calibrationmeasurements",
            name="time_c_i",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="calibrationmeasurements",
            name="time_c_ii",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="calibrationmeasurements",
            name="time_m21",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="calibrationmeasurements",
            name="time_m31",
            field=models.FloatField(default=0.0),
        ),
    ]

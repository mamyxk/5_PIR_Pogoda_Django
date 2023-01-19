# Generated by Django 4.1.5 on 2023-01-19 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sensor",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=20)),
                ("description", models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name="SensorLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("temperature", models.FloatField()),
                ("humidity", models.FloatField()),
                ("created_at", models.DateTimeField()),
                (
                    "sensor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="sensors.sensor"
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 4.1.5 on 2023-01-20 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0002_sensorlog_altitude_sensorlog_pressure_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorlog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

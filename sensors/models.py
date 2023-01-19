from django.db import models

# Create your models here.

class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=300)

class SensorLog(models.Model):
    sensor = models.ForeignKey(Sensor,on_delete=models.PROTECT)
    temperature = models.FloatField()
    humidity = models.FloatField()
    created_at = models.DateTimeField()
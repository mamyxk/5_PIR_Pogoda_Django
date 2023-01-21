from django.db import models

# Create your models here.

class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.id}: {self.name}"

class SensorLog(models.Model):
    sensor = models.ForeignKey(Sensor,on_delete=models.PROTECT)
    temperature = models.FloatField()
    pressure = models.FloatField()
    humidity = models.FloatField()
    altitude = models.FloatField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor}: temp: {self.temperature} | press: {self.pressure} | hum: {self.humidity} | alt: {self.altitude}"
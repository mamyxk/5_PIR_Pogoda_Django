from rest_framework import serializers
from sensors.models import SensorLog

class SensorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorLog
        fields = '__all__'

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from .serializers import SensorLogSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from sensors.models import Sensor 
from sensors.models import SensorLog

import json

# Create your views here.

def index(request):
    try:
        sensors = Sensor.objects.all()
    except Sensor.DoesNotExist:
        raise Http404("Sensor does not exist")
    return render(request, 'sensors/index.html', {'sensors': sensors})

@api_view(['POST'])
def fetch_sensor_logs(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            sensor_ids = data.get('selectedSensors')
            sensor_logs = list(SensorLog.objects.filter(sensor_id__in=sensor_ids).order_by('-timestamp')[:20].values())
            return JsonResponse({'context': sensor_logs})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

@api_view(['POST'])
def add_sensor_log(request):
    if request.method == 'POST':
        serializer = SensorLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
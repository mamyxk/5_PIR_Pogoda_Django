from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
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
            response = { sensor_id: list(SensorLog.objects.filter(sensor_id=sensor_id).order_by('-timestamp')[:20].values()) for sensor_id in sensor_ids }
            return JsonResponse({'context': response})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

@api_view(['POST'])
def fetch_sensor_name(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            requested_id = json.load(request).get('sensor_id')
            response = Sensor.objects.filter(id=requested_id)[0].name
            return JsonResponse({'sensor_name': response})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

@api_view(['POST'])
def add_sensor_log(request):
    if request.method != 'POST':
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer = SensorLogSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

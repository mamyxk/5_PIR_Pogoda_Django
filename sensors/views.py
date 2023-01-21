from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .serializers import SensorLogSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def index(request):
    return render(request, 'sensors/index.html')

@api_view(['POST'])
def add_sensor_log(request):
    if request.method == 'POST':
        serializer = SensorLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
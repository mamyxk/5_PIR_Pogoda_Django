from django.urls import URLPattern, path, include
from . import views


urlpatterns = [
    path('',views.index),
    path('add_sensor_log', views.add_sensor_log),
    path('fetch_sensor_logs', views.fetch_sensor_logs)
]
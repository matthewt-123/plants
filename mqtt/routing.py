from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from mqtt.consumers import SensorConsumer
application =[
    path('ws/sensors', SensorConsumer.as_asgi()),
]
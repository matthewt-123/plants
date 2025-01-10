import json
from .models import MQTTError
from datetime import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class SensorConsumer(WebsocketConsumer):
    #GROUP NAME: sensors
    #TYPE NAME: data.notif
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'sensors',
            self.channel_name
        )
        self.groups.append("sensors")
        self.accept()
        MQTTError.objects.create(module='ws', event='connect', message='connected', error=False, time=datetime.now())


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'sensors',
            self.channel_name
        )
        print("CLOSING")
        print(close_code)
        MQTTError.objects.create(module='ws', event='disconnect', message='disconnected', error=False, time=datetime.now())

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

    def data_notif(self, event):
        self.send(text_data=json.dumps({
                'type': 'data.notif',
                'module': event['module'],
                'content': event['content'],
            })
        )
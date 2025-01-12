import random
from paho.mqtt import client as mqtt_client
from .models import Plant, MQTTError, SensorData
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import os
import sys
import json

sys.path.append('..')
from smvDashboard.settings import ip_address
topics = ["plants/sensorData"]
curr_plant = 0
lightLevels = {"Low": 0, "Moderate": 1, "High": 2}

def get_plant():
    if curr_plant == 0:
        return Plant.objects.last()
    return curr_plant
def set_plant(plantType):
    curr_plant = plantType

broker = ip_address
port = 1883
global CLIENT
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'matthew'
password = os.environ.get("MQTT_PW")

def connect_mqtt(client_id=client_id) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            MQTTError.objects.create(module='mqtt', event='connect', message='connected', error=False, time=datetime.now())
        else:
            #error state
            MQTTError.objects.create(module='mqtt', event='connect', message=f"Failed to connect, return code {rc}, client: {client}\n", error=True, time=datetime.now(), trip=Trip.objects.last())
            return None
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def store(msg):
    channel_layer = get_channel_layer()

    try:
        sensors = json.loads(msg.payload.decode())
        print(sensors)
        sensorOutput = SensorData.objects.create(date=datetime.now(), plant=get_plant(), temperature=sensors['temperature'], humidity=sensors['humidity'], light=sensors['light']) 
        lightReading, adjustLight, adjustTemp, adjustHumidity = runAnalysis(sensorOutput)
        async_to_sync(channel_layer.group_send)("sensors", {"type": f"data.notif", "module": f"humidity", "content": sensors['humidity']})
        async_to_sync(channel_layer.group_send)("sensors", {"type": f"data.notif", "module": f"temperature", "content": sensors['temperature']})
        async_to_sync(channel_layer.group_send)("sensors", {"type": f"data.notif", "module": f"light", "content": sensors['light']})
        async_to_sync(channel_layer.group_send)("sensors", {"type": f"data.notif", "module": f"light", "content": lightReading})
    except Exception as e:
        #on error, pass. log error in MQTT Error Log
        print(e)
        MQTTError.objects.create(module='mqtt', event='receive', message=f'{e}', error=True, time=datetime.now())


def subscribe(topic, client: mqtt_client):
    def on_message(client, userdata, msg):
        store(msg)
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    if client:
        for topic in topics:
            subscribe(topic, client)
        client.loop_forever()
    else:
        run()

def publish(topic, message):
    client = connect_mqtt(client_id=f'subscribe-{random.randint(0, 1000)}')
    client.publish(topic, message)

def runAnalysis(sensorOutput):

    # LIGHT 

    if sensorOutput.light < 1.0:
        lightReading = "Low"
    elif sensorOutput.light < 1.5:
        lightReading = "Moderate"
    else:
        lightReading = "High"
    print("l1")
    if lightLevels[lightReading] < sensorOutput.plant.sunlight:
        adjustLight = "Light level is lower than normal. If possible, move plant into direct sunlight."
    if sensorOutput.light == sensorOutput.plant.sunlight:
        adjustLight = "Light level is normal."
    if sensorOutput.light > sensorOutput.plant.sunlight:
        adjustLight = "Light level is higher than normal. If possible, move plant away from direct sunlight."
    print("light")
    # TEMPERATURE

    if sensorOutput.temperature < sensorOutput.plant.minTemperature:
        adjustTemp = "Temperature is lower than normal."
    elif sensorOutput.temperature > sensorOutput.plant.maxTemperature:
        adjustTemp = "Temperature is higher than normal."
    else:
        adjustTemp = "Temperature is normal."
    print("tmp")

    # HUMIDITY

    if sensorOutput.humidity < sensorOutput.plant.minHumidity:
        adjustHumidity = "Humidity is lower than normal."
    elif sensorOutput.humidity > sensorOutput.plant.maxHumidity:
        adjustHumidity = "Humidity is higher than normal."
    else:
        adjustHumidity = "Humidity is normal."
    print("humid")

    return lightReading, adjustLight, adjustTemp, adjustHumidity


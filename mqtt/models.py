from django.db import models
import sys
sys.path.append("..")
# Create your models here.
    
class Plant(models.Model):
    name = models.CharField(max_length=128, default="", blank="", null="")
    sunlight = models.DecimalField(max_digits=6, decimal_places=3)
    water = models.DecimalField(max_digits=6, decimal_places=3)
    soil_type = models.DecimalField(max_digits=6, decimal_places=3)
    humidity = models.DecimalField(max_digits=6, decimal_places=3)
    active = models.BooleanField(default=False)
    lore = models.TextField()
    date_created = models.DateField()
    def __str__(self):
        return f"  Plant"

#set: powerMessage
class SensorData(models.Model):
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE)
    humidity = models.DecimalField(max_digits=6, decimal_places=3)
    temperature = models.DecimalField(max_digits=6, decimal_places=3)
    light = models.DecimalField(max_digits=6, decimal_places=3)
    date = models.DateTimeField()
    class Meta:
        verbose_name_plural = "  Sensor Data" 

#extra data
class MessageHistory(models.Model):
    topic = models.CharField(max_length=128)
    message = models.TextField()
    date = models.DateTimeField()
    def __str__(self):
        return self.topic
class MQTTError(models.Model):
    module = models.CharField(max_length=30, choices = (("mqtt", "mqtt"), ("ws", "ws")))
    event = models.CharField(max_length=30, choices = (("connect", "connect"), ("disconnect", "disconnect"), ("receive_message", "receive_message")))
    message = models.TextField()
    error = models.BooleanField()
    time = models.DateTimeField()
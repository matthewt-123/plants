from django.contrib import admin
from .models import MessageHistory, SensorData, Plant, MQTTError
#columns
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "date")
class PlantAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "humidity", "temperature", "light", "plant")
# Register your models here.
admin.site.register(SensorData, SensorDataAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(MessageHistory, MessageHistoryAdmin)
admin.site.register(MQTTError)

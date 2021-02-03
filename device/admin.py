from django.contrib import admin
from .models import Service, Device, DeviceSchedule, PointedSchedule

admin.site.register(Service)
admin.site.register(Device)
admin.site.register(DeviceSchedule)
admin.site.register(PointedSchedule)
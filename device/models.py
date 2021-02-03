from django.db import models
from pacient.models import Pacient

class Service(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    duration = models.IntegerField()

    def __str__(self):
        return self.name+'_'+str(self.duration)

class Device(models.Model):
    name = models.CharField(max_length=255)
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.name

lst = []
for i in range(1, 161):
    lst.append('meet' + str(i))

class DeviceSchedule(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    for label in lst:
        locals()[label] = models.CharField(max_length=128, default='-')
    del locals()['label']

    def __str__(self):
        return self.device.name

class PointedSchedule(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    duration = models.IntegerField(blank=True, default=0)
    date = models.DateField()
    time = models.TimeField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.device.name+'_'+self.pacient.fullname.split()[0].lower()+'_'+str(self.duration)
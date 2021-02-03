from django.db import models
from resource.models import Specialty, Doctor

class Pacient(models.Model):
    fullname = models.CharField(max_length=255)
    specialty = models.ManyToManyField(Specialty)

    def __str__(self):
        return self.fullname.lower()

class Schedule(models.Model):
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.pacient.fullname.split()[0].lower()+'_'+self.doctor.specialty.specialty_code

# class Group(models.Model):
#     group_name = models.CharField(max_length=255)
#     pacient = models.ManyToManyField(Pacient)
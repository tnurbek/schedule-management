from django.db import models

class Specialty(models.Model):
    specialty_name = models.CharField(max_length=255)
    specialty_code = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.specialty_name

class Doctor(models.Model):
    fullname = models.CharField(max_length=512)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.fullname.split()[0].lower()

lst = []
for i in range(1, 161):
    lst.append('meet' + str(i))

class ScheduleDoctor(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=128)
    for label in lst:
        locals()[label] = models.CharField(max_length=128, default='-')
    del locals()['label']

    def __str__(self):
        return self.doctor.fullname.split()[0].lower()+'_'+self.doctor.fullname.split()[1].lower()+'_'+self.weekday
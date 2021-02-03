from django.db import models

class Action(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='files')

    def __str__(self):
        return self.title

class Pacient_Schedule(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='results')
    pacients_file = models.ForeignKey(Action, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
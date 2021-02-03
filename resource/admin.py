from django.contrib import admin
from .models import Specialty, Doctor, ScheduleDoctor

admin.site.register(Specialty)
admin.site.register(Doctor)
admin.site.register(ScheduleDoctor)
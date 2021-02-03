from django.urls import path
from . import views

urlpatterns = [
    path('', views.devices_home, name='devices_home'),
    path('<int:pk>', views.device, name='device'),
    path('<int:pk>/secondary', views.device2, name='device2'),
    path('<int:pk>/<int:weekday>', views.device_weekday, name='device_weekday'),
    path('<int:pk>/secondary/<int:weekday>', views.device_weekday2, name='device_weekday2'),
    path('set_schedule', views.set_schedule, name='set_schedule'),
    path('reg_device_pacient/<int:pk>', views.reg_device_pacients, name='reg_device_pacients'),
    path('get_services_of_device', views.get_services_of_device, name='get_services_of_device'),
    path('getdates_of_device', views.getdates_of_device, name='getdates_of_device'),
    path('get_available_times_device', views.get_available_times_device, name='get_available_times_device'),
    path('reg_device_pacient/<int:pk>/save_device_schedule', views.save_device_schedule, name='save_device_schedule'),
    path('reg_device_pacient/save_device_schedule2', views.save_device_schedule2, name='save_device_schedule2'),
    path('get_specific_time_info', views.get_specific_time_info, name='get_specific_time_info'),
    path('pointed_schedule/<int:pk>', views.pointed_schedule, name='pointed_schedule'),
    path('patient_statistics', views.patient_statistics, name='patient_statistics'),
]
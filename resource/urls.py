from django.urls import path
from . import views

urlpatterns = [
    path('', views.coordinator_page, name='coordinator_page'),
    path('save_schedule', views.save_schedule, name='save_schedule'),
    path('doctors_schedule', views.doctors_schedule, name='schedule'),
    path('doctors_schedule/<int:pk>', views.specific_schedule, name='specific_schedule'),
    path('doctor_info', views.doctor_info, name='doctor_info'),
    path('get_duration', views.get_duration, name='get_duration'),
    path('get_times', views.get_times, name='get_times'),
    path('doctors_search', views.doctors_search, name='doctors_search'),
]
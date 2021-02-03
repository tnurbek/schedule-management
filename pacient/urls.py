from django.urls import path
from . import views

urlpatterns = [
    path('', views.pacients_home, name='pacients_home'),
    path('<int:pk>', views.specific_pacient, name='specific_pacient'),
    path('create', views.create_pacient, name='create_pacient'),
    path('getdocs_by_spec', views.getdocs_by_spec, name='getdocs_by_spec'),
    path('getdates_by_doc', views.getdates_by_doc, name='getdates_by_doc'),
    path('get_available_times', views.get_available_times, name='get_available_times'),
    path('<int:pk>/save_schedule', views.save_schedule, name='save_schedule'),
    path('controller', views.control, name='controller'),
    path('controller/meeting_done', views.meeting_done, name='meeting_done'),
]
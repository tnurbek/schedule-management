"""schedule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from action import views
from account import views as auth_views
from django.contrib.auth import views as auth_vs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('upload', views.upload, name='upload'),
    path('schedules', views.list_schedule, name='list_schedule'),
    path('schedule/<int:action_id>', views.schedule, name='schedule'),
    path('result/<int:action_id>', views.get_result, name='getresult'),
    # authorization and authentication
    path('signup', auth_views.SignUp.as_view(), name='signup'),
    path('signin', auth_vs.LoginView.as_view(), name='signin'),
    path('signout', auth_vs.LogoutView.as_view(), name='signout'),
    # resource
    path('resources/', include('resource.urls')),
    # patients
    path('patients/', include('pacient.urls')),
    # devices
    path('devices/', include('device.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL configuration for salon_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
"""Top-level URL configuration for the salon booking project."""

from django.contrib import admin
from django.urls import include, path
from appointments.views import dashboard
from accounts.views import admin_logout_redirect

urlpatterns = [
    path('admin/logout/', admin_logout_redirect, name='admin_logout'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('services/', include('services.urls')),
    path('masters/', include('masters.urls')),
    path('appointments/', include('appointments.urls')),
    path('', dashboard, name='home'),
]

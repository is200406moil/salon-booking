"""URL routes for appointment booking pages."""

from django.urls import path

from .views import (
    admin_appointments,
    appointment_cancel,
    appointment_detail,
    appointment_update,
    booking_step,
    dashboard,
)

app_name = "appointments"


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("booking/", booking_step, name="booking"),
    path("<int:pk>/", appointment_detail, name="appointment_detail"),
    path("<int:pk>/edit/", appointment_update, name="appointment_update"),
    path("<int:pk>/cancel/", appointment_cancel, name="appointment_cancel"),
    path("admin/list/", admin_appointments, name="admin_list"),
]
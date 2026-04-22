"""Admin configuration for appointment records."""

from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Admin configuration for appointments.

    Description:
        Adds list display and filters for appointment management.

    Args:
        admin.ModelAdmin: Django admin base class.

    Returns:
        None

    Raises:
        None

    Examples:
        >>> AppointmentAdmin.list_display
        ('client', 'master', 'service')
    """

    list_display = ("client", "master", "service", "status", "created_at")
    list_filter = ("status", "service", "master")
    search_fields = ("client__username", "client__first_name", "client__last_name")

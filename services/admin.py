"""Admin configuration for service models."""

from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin configuration for services.

    Description:
        Adds list display and search for service management in admin.

    Args:
        admin.ModelAdmin: Django admin base class.

    Returns:
        None

    Raises:
        None

    Examples:
        >>> ServiceAdmin.search_fields
        ('name',)
    """

    list_display = ("name", "price", "duration_minutes", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)

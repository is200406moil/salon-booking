"""Admin configuration for master profiles and working slots."""

from django.contrib import admin

from .models import MasterProfile, WorkingSlot


@admin.register(MasterProfile)
class MasterProfileAdmin(admin.ModelAdmin):
    """Admin configuration for master profiles.

    Description:
        Provides list display and filtering for master management.

    Args:
        admin.ModelAdmin: Django admin base class.

    Returns:
        None

    Raises:
        None

    Examples:
        >>> MasterProfileAdmin.list_display
        ('user', 'is_active')
    """

    list_display = ("user", "is_active")
    list_filter = ("is_active",)
    search_fields = ("user__username", "user__first_name", "user__last_name")
    filter_horizontal = ("services",)


@admin.register(WorkingSlot)
class WorkingSlotAdmin(admin.ModelAdmin):
    """Admin configuration for working slots.

    Description:
        Shows slot timing and availability in the admin interface.

    Args:
        admin.ModelAdmin: Django admin base class.

    Returns:
        None

    Raises:
        None

    Examples:
        >>> WorkingSlotAdmin.list_display
        ('master', 'start_at', 'end_at', 'is_available')
    """

    list_display = ("master", "start_at", "end_at", "is_available")
    list_filter = ("is_available", "master")
    search_fields = ("master__user__username",)

"""Admin configuration for user accounts."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class SalonUserAdmin(UserAdmin):
    """Admin settings for custom User model.

    Description:
        Extends Django's ``UserAdmin`` to show role and phone fields.

    Args:
        UserAdmin (ModelAdmin): Django admin class for users.

    Returns:
        None

    Raises:
        None

    Examples:
        >>> SalonUserAdmin.list_display
        ('username', 'email', 'role', 'is_staff')
    """

    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = list(UserAdmin.fieldsets) + [
        ("Дополнительные данные", {"fields": ("role", "phone")}),
    ]

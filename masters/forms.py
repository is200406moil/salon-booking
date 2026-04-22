"""Forms for managing master profiles and working slots."""

from django import forms

from .models import MasterProfile, WorkingSlot


class MasterProfileForm(forms.ModelForm):
    """Form for creating and updating master profiles.

    Description:
        Allows administrators to manage master profile details and services.

    Args:
        forms.ModelForm: Base model form class.

    Returns:
        MasterProfileForm: Configured form instance.

    Raises:
        forms.ValidationError: Raised when validation fails.

    Examples:
        >>> form = MasterProfileForm()
        >>> "services" in form.fields
        True
    """

    class Meta:
        """Metadata for the master profile form."""

        model = MasterProfile
        fields = ("user", "bio", "services", "is_active")


class WorkingSlotForm(forms.ModelForm):
    """Form for creating and updating working slots.

    Description:
        Used by administrators to define available time slots for masters.

    Args:
        forms.ModelForm: Base model form class.

    Returns:
        WorkingSlotForm: Configured form instance.

    Raises:
        forms.ValidationError: Raised when validation fails.

    Examples:
        >>> form = WorkingSlotForm()
        >>> "start_at" in form.fields
        True
    """

    class Meta:
        """Metadata for the working slot form."""

        model = WorkingSlot
        fields = ("master", "start_at", "end_at", "is_available")
        widgets = {
            "start_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
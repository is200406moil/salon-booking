"""Forms for appointment booking and management."""

from django import forms

from masters.models import WorkingSlot
from services.models import Service

from .models import Appointment


class AppointmentCreateForm(forms.ModelForm):
    """Form for clients to create a new appointment.

    Description:
        Enables a client to choose a service, master slot, and add notes.
        Slot list should be filtered in the view to show only available ones.

    Args:
        forms.ModelForm: Base model form class.

    Returns:
        AppointmentCreateForm: Configured form instance.

    Raises:
        forms.ValidationError: Raised when validation fails.

    Examples:
        >>> form = AppointmentCreateForm()
        >>> "service" in form.fields
        True
    """

    service = forms.ModelChoiceField(queryset=Service.objects.none(), label="Услуга")
    slot = forms.ModelChoiceField(queryset=WorkingSlot.objects.none(), label="Свободное время")

    class Meta:
        """Metadata for the appointment create form."""

        model = Appointment
        fields = ("service", "slot", "notes")

    def __init__(self, *args, **kwargs):
        """Initialize form with filtered querysets.

        Description:
            Ensures only active services and available slots are displayed.

        Args:
            *args: Positional arguments for the base form.
            **kwargs: Keyword arguments for the base form.

        Returns:
            None

        Raises:
            None

        Examples:
            >>> form = AppointmentCreateForm()
            >>> form.fields["service"].queryset.model.__name__
            'Service'
        """

        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = Service.objects.filter(is_active=True)
        self.fields["slot"].queryset = WorkingSlot.objects.filter(is_available=True)


class AppointmentUpdateForm(forms.ModelForm):
    """Form for rescheduling or updating an appointment.

    Description:
        Allows a client to update the slot and notes for an existing booking.

    Args:
        forms.ModelForm: Base model form class.

    Returns:
        AppointmentUpdateForm: Configured form instance.

    Raises:
        forms.ValidationError: Raised when validation fails.

    Examples:
        >>> form = AppointmentUpdateForm()
        >>> "slot" in form.fields
        True
    """

    slot = forms.ModelChoiceField(queryset=WorkingSlot.objects.none(), label="Новое время")

    class Meta:
        """Metadata for the appointment update form."""

        model = Appointment
        fields = ("slot", "notes")

    def __init__(self, *args, **kwargs):
        """Initialize form with available slots.

        Description:
            Filters slots to those that are currently available.

        Args:
            *args: Positional arguments for the base form.
            **kwargs: Keyword arguments for the base form.

        Returns:
            None

        Raises:
            None

        Examples:
            >>> form = AppointmentUpdateForm()
            >>> form.fields["slot"].queryset.model.__name__
            'WorkingSlot'
        """

        super().__init__(*args, **kwargs)
        self.fields["slot"].queryset = WorkingSlot.objects.filter(is_available=True)
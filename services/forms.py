"""Forms for salon service management."""

from django import forms

from .models import Service


class ServiceForm(forms.ModelForm):
    """Form for creating and updating services.

    Description:
        Provides a form for administrators to manage salon services.

    Args:
        forms.ModelForm: Base model form class.

    Returns:
        ServiceForm: Configured form instance.

    Raises:
        forms.ValidationError: Raised when validation fails.

    Examples:
        >>> form = ServiceForm()
        >>> "name" in form.fields
        True
    """

    class Meta:
        """Metadata for the service form."""

        model = Service
        fields = ("name", "description", "duration_minutes", "price", "is_active")
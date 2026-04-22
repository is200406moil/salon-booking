"""Forms for authentication and user profile management."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class ClientRegistrationForm(UserCreationForm):
    """Form for registering a new client account.

    Description:
        Extends Django's default user creation form to include email and phone
        fields and pre-assigns the client role.

    Args:
        UserCreationForm (forms.ModelForm): Base Django registration form.

    Returns:
        ClientRegistrationForm: Configured form instance.

    Raises:
        forms.ValidationError: Raised when validation fails.

    Examples:
        >>> form = ClientRegistrationForm(data={"username": "anna"})
        >>> form.is_valid()
        False
    """

    class Meta(UserCreationForm.Meta):
        """Metadata for the registration form."""

        model = User
        fields = ("username", "first_name", "last_name", "email", "phone")

    def save(self, commit: bool = True) -> User:
        """Save the user instance with the client role.

        Description:
            Assigns ``User.Role.CLIENT`` to the user before saving.

        Args:
            commit (bool): Whether to save the instance immediately.

        Returns:
            User: The created user instance.

        Raises:
            None

        Examples:
            >>> form = ClientRegistrationForm(data={})
            >>> isinstance(form.save(commit=False), User)
            True
        """

        user = super().save(commit=False)
        user.role = User.Role.CLIENT
        if commit:
            user.save()
        return user


class SalonAuthenticationForm(AuthenticationForm):
    """Custom authentication form for salon users.

    Description:
        Keeps Django authentication behavior but provides a separate class
        for explicit documentation and styling in templates.

    Args:
        AuthenticationForm (forms.Form): Django authentication form.

    Returns:
        SalonAuthenticationForm: Configured form instance.

    Raises:
        forms.ValidationError: Raised when authentication fails.

    Examples:
        >>> form = SalonAuthenticationForm()
        >>> form.fields["username"].label
        'Username'
    """


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating client profile information.

    Description:
        Allows clients to update their contact information in the personal
        dashboard.

    Args:
        forms.ModelForm: Base model form class.

    Returns:
        ProfileUpdateForm: Configured form instance.

    Raises:
        forms.ValidationError: Raised when validation fails.

    Examples:
        >>> form = ProfileUpdateForm()
        >>> "phone" in form.fields
        True
    """

    class Meta:
        """Metadata for profile update form."""

        model = User
        fields = ("first_name", "last_name", "email", "phone")
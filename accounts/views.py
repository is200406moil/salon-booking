"""Views for authentication and user profile actions."""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import ClientRegistrationForm, ProfileUpdateForm, SalonAuthenticationForm


class SalonLoginView(LoginView):
    """Render the login form and authenticate users.

    Description:
        Uses Django's built-in login view with a custom form and template
        styling consistent with the salon UI.

    Args:
        LoginView (View): Django authentication login view.

    Returns:
        HttpResponse: Rendered login page or redirect on success.

    Raises:
        PermissionDenied: When access is denied.

    Examples:
        >>> view = SalonLoginView()
        >>> view.template_name
        'accounts/login.html'
    """

    template_name = "accounts/login.html"
    authentication_form = SalonAuthenticationForm

    def get_success_url(self):
        """Return the URL to redirect users after successful login.

        Description:
            Redirects administrators to Django admin and other users to the
            client dashboard.

        Args:
            None

        Returns:
            str: URL for the next page after login.

        Raises:
            None

        Examples:
            >>> view = SalonLoginView()
            >>> isinstance(view.get_success_url(), str)
            True
        """

        user = self.request.user
        if user.is_staff or getattr(user, "is_admin", False):
            return reverse_lazy("admin:index")
        return reverse_lazy("appointments:dashboard")


class SalonLogoutView(LogoutView):
    """Log out the current user.

    Description:
        Clears the session and redirects to the login page.

    Args:
        LogoutView (View): Django authentication logout view.

    Returns:
        HttpResponseRedirect: Redirect to the login page.

    Raises:
        None

    Examples:
        >>> view = SalonLogoutView()
        >>> view.next_page
        '/accounts/login/'
    """

    next_page = reverse_lazy("accounts:login")
    http_method_names = ["get", "post", "head", "options"]


def logout_redirect(request):
    """Log out the current user and redirect to login.

    Description:
        Provides a guaranteed redirect to the login page regardless of
        logout source (client or admin).

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponseRedirect: Redirect to the login page.

    Raises:
        None

    Examples:
        >>> response = logout_redirect(request)
        >>> response.status_code
        302
    """

    logout(request)
    return redirect("accounts:login")


def register(request):
    """Register a new client account.

    Description:
        Handles client registration, creates the user, and logs them in.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered registration template or redirect.

    Raises:
        None

    Examples:
        >>> response = register(request)
        >>> response.status_code
        200
    """

    if request.method == "POST":
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация выполнена успешно.")
            return redirect("appointments:dashboard")
    else:
        form = ClientRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    """Display and update the client profile.

    Description:
        Allows the authenticated client to update personal information.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered profile page or redirect.

    Raises:
        None

    Examples:
        >>> response = profile(request)
        >>> response.status_code
        200
    """

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлен.")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


def admin_logout_redirect(request):
    """Log out from Django admin and redirect to the login page.

    Description:
        Ensures administrators are redirected to the standard login form
        instead of the default admin logout page.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponseRedirect: Redirect to the accounts login page.

    Raises:
        None

    Examples:
        >>> response = admin_logout_redirect(request)
        >>> response.status_code
        302
    """

    logout(request)
    return redirect("accounts:login")
"""Views for displaying and managing salon services."""

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ServiceForm
from .models import Service


def service_list(request):
    """Display the list of active services.

    Description:
        Shows the catalog of services to clients and staff.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered service list page.

    Raises:
        None

    Examples:
        >>> response = service_list(request)
        >>> response.status_code
        200
    """

    services = Service.objects.filter(is_active=True)
    return render(request, "services/service_list.html", {"services": services})


def _is_admin(user):
    """Check whether the user has administrative privileges.

    Description:
        Used as a decorator helper for administrative views.

    Args:
        user (User): Authenticated user instance.

    Returns:
        bool: ``True`` when user is staff or has admin role.

    Raises:
        None

    Examples:
        >>> _is_admin(user)
        False
    """

    return user.is_authenticated and (user.is_staff or getattr(user, "is_admin", False))


@login_required
@user_passes_test(_is_admin)
def service_create(request):
    """Create a new service entry.

    Description:
        Allows administrators to add new salon services.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered creation form or redirect.

    Raises:
        None

    Examples:
        >>> response = service_create(request)
        >>> response.status_code
        200
    """

    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("services:admin_list")
    else:
        form = ServiceForm()
    return render(request, "services/service_form.html", {"form": form, "action": "Создать"})


@login_required
@user_passes_test(_is_admin)
def service_update(request, pk):
    """Update an existing service.

    Description:
        Allows administrators to edit service details.

    Args:
        request (HttpRequest): Incoming HTTP request.
        pk (int): Primary key of the service.

    Returns:
        HttpResponse: Rendered edit form or redirect.

    Raises:
        Http404: If the service does not exist.

    Examples:
        >>> response = service_update(request, 1)
        >>> response.status_code
        200
    """

    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect("services:admin_list")
    else:
        form = ServiceForm(instance=service)
    return render(request, "services/service_form.html", {"form": form, "action": "Обновить"})


@login_required
@user_passes_test(_is_admin)
def service_delete(request, pk):
    """Delete a service entry.

    Description:
        Allows administrators to remove services.

    Args:
        request (HttpRequest): Incoming HTTP request.
        pk (int): Primary key of the service.

    Returns:
        HttpResponse: Confirmation page or redirect.

    Raises:
        Http404: If the service does not exist.

    Examples:
        >>> response = service_delete(request, 1)
        >>> response.status_code
        200
    """

    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.delete()
        return redirect("services:admin_list")
    return render(request, "services/service_confirm_delete.html", {"service": service})


@login_required
@user_passes_test(_is_admin)
def service_admin_list(request):
    """Administrative list of services.

    Description:
        Displays all services for management by the administrator.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered admin list.

    Raises:
        None

    Examples:
        >>> response = service_admin_list(request)
        >>> response.status_code
        200
    """

    services = Service.objects.all()
    return render(request, "services/service_admin_list.html", {"services": services})

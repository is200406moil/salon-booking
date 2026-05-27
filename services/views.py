"""Views for displaying and managing salon services."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from appointments.models import Appointment
from masters.models import WorkingSlot

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

    if request.method == "POST":
        if not request.user.is_authenticated:
            login_url = f"{reverse('accounts:login')}?next={request.path}"
            return redirect(login_url)
        service_id = request.POST.get("service_id")
        slot_id = request.POST.get("slot_id")
        notes = (request.POST.get("notes") or "").strip()
        service = Service.objects.filter(pk=service_id, is_active=True).first()
        slot = (
            WorkingSlot.objects.filter(
                pk=slot_id,
                is_available=True,
                master__is_active=True,
            )
            .select_related("master")
            .first()
        )
        if not service or not slot or not slot.master.services.filter(pk=service.pk).exists():
            messages.error(request, "Проверьте выбранную услугу и свободный слот.")
            return redirect(reverse("services:list"))
        Appointment.objects.create(
            client=request.user,
            master=slot.master,
            service=service,
            slot=slot,
            notes=notes,
        )
        slot.is_available = False
        slot.save(update_fields=["is_available"])
        messages.success(request, "Запись создана.")
        return redirect(f"{reverse('services:list')}#service-{service.pk}")

    services = list(
        Service.objects.filter(is_active=True).prefetch_related("masters__user")
    )
    slots = (
        WorkingSlot.objects.filter(
            is_available=True,
            master__is_active=True,
            master__services__in=services,
        )
        .select_related("master__user")
        .prefetch_related("master__services")
        .order_by("start_at")
        .distinct()
    )
    slots_by_service = {service.id: [] for service in services}
    for slot in slots:
        for service in slot.master.services.all():
            if service.id in slots_by_service:
                slots_by_service[service.id].append(slot)
    for service in services:
        service.available_slots = slots_by_service.get(service.id, [])
        service.master_count = service.masters.filter(is_active=True).count()
    base_template = "base_dashboard.html" if request.user.is_authenticated else "base.html"
    return render(
        request,
        "services/service_list.html",
        {"services": services, "base_template": base_template},
    )


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

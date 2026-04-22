"""Views for master profiles and working schedules."""

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MasterProfileForm, WorkingSlotForm
from .models import MasterProfile, WorkingSlot


def _is_admin(user):
    """Check whether the user has administrative privileges.

    Description:
        Ensures only admins or staff users can manage master data.

    Args:
        user (User): Authenticated user instance.

    Returns:
        bool: ``True`` when user is staff or admin.

    Raises:
        None

    Examples:
        >>> _is_admin(user)
        False
    """

    return user.is_authenticated and (user.is_staff or getattr(user, "is_admin", False))


def master_list(request):
    """Display the list of active masters.

    Description:
        Shows masters and their offered services to clients.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered master list page.

    Raises:
        None

    Examples:
        >>> response = master_list(request)
        >>> response.status_code
        200
    """

    masters = MasterProfile.objects.filter(is_active=True)
    return render(request, "masters/master_list.html", {"masters": masters})


@login_required
def master_schedule(request):
    """Show the schedule for the logged-in master.

    Description:
        Displays appointments and available slots for the master.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered schedule page.

    Raises:
        MasterProfile.DoesNotExist: If profile is missing for the user.

    Examples:
        >>> response = master_schedule(request)
        >>> response.status_code
        200
    """

    profile = get_object_or_404(MasterProfile, user=request.user)
    slots = profile.working_slots.select_related("master")
    appointments = profile.appointments.select_related("client", "service", "slot")
    return render(
        request,
        "masters/master_schedule.html",
        {"profile": profile, "slots": slots, "appointments": appointments},
    )


@login_required
@user_passes_test(_is_admin)
def master_admin_list(request):
    """Administrative list of master profiles.

    Description:
        Displays all master profiles for admin management.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered admin list.

    Raises:
        None

    Examples:
        >>> response = master_admin_list(request)
        >>> response.status_code
        200
    """

    masters = MasterProfile.objects.all()
    return render(request, "masters/master_admin_list.html", {"masters": masters})


@login_required
@user_passes_test(_is_admin)
def master_create(request):
    """Create a master profile.

    Description:
        Allows administrators to create new master profiles.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered creation form or redirect.

    Raises:
        None

    Examples:
        >>> response = master_create(request)
        >>> response.status_code
        200
    """

    if request.method == "POST":
        form = MasterProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("masters:admin_list")
    else:
        form = MasterProfileForm()
    return render(request, "masters/master_form.html", {"form": form, "action": "Создать"})


@login_required
@user_passes_test(_is_admin)
def master_update(request, pk):
    """Update a master profile.

    Description:
        Allows administrators to edit master details.

    Args:
        request (HttpRequest): Incoming HTTP request.
        pk (int): Primary key of the master profile.

    Returns:
        HttpResponse: Rendered edit form or redirect.

    Raises:
        Http404: If the master does not exist.

    Examples:
        >>> response = master_update(request, 1)
        >>> response.status_code
        200
    """

    master = get_object_or_404(MasterProfile, pk=pk)
    if request.method == "POST":
        form = MasterProfileForm(request.POST, instance=master)
        if form.is_valid():
            form.save()
            return redirect("masters:admin_list")
    else:
        form = MasterProfileForm(instance=master)
    return render(request, "masters/master_form.html", {"form": form, "action": "Обновить"})


@login_required
@user_passes_test(_is_admin)
def master_delete(request, pk):
    """Delete a master profile.

    Description:
        Allows administrators to remove a master profile.

    Args:
        request (HttpRequest): Incoming HTTP request.
        pk (int): Primary key of the master profile.

    Returns:
        HttpResponse: Confirmation page or redirect.

    Raises:
        Http404: If the master does not exist.

    Examples:
        >>> response = master_delete(request, 1)
        >>> response.status_code
        200
    """

    master = get_object_or_404(MasterProfile, pk=pk)
    if request.method == "POST":
        master.delete()
        return redirect("masters:admin_list")
    return render(request, "masters/master_confirm_delete.html", {"master": master})


@login_required
@user_passes_test(_is_admin)
def slot_admin_list(request):
    """Administrative list of working slots.

    Description:
        Displays all working slots for schedule management.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered slot list.

    Raises:
        None

    Examples:
        >>> response = slot_admin_list(request)
        >>> response.status_code
        200
    """

    slots = WorkingSlot.objects.select_related("master", "master__user")
    return render(request, "masters/slot_admin_list.html", {"slots": slots})


@login_required
@user_passes_test(_is_admin)
def slot_create(request):
    """Create a new working slot for a master.

    Description:
        Allows administrators to define available time slots.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered creation form or redirect.

    Raises:
        None

    Examples:
        >>> response = slot_create(request)
        >>> response.status_code
        200
    """

    if request.method == "POST":
        form = WorkingSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("masters:slot_list")
    else:
        form = WorkingSlotForm()
    return render(request, "masters/slot_form.html", {"form": form, "action": "Создать"})


@login_required
@user_passes_test(_is_admin)
def slot_update(request, pk):
    """Update an existing working slot.

    Description:
        Allows administrators to modify slot details.

    Args:
        request (HttpRequest): Incoming HTTP request.
        pk (int): Primary key of the slot.

    Returns:
        HttpResponse: Rendered edit form or redirect.

    Raises:
        Http404: If the slot does not exist.

    Examples:
        >>> response = slot_update(request, 1)
        >>> response.status_code
        200
    """

    slot = get_object_or_404(WorkingSlot, pk=pk)
    if request.method == "POST":
        form = WorkingSlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            return redirect("masters:slot_list")
    else:
        form = WorkingSlotForm(instance=slot)
    return render(request, "masters/slot_form.html", {"form": form, "action": "Обновить"})


@login_required
@user_passes_test(_is_admin)
def slot_delete(request, pk):
    """Delete a working slot.

    Description:
        Allows administrators to remove a slot.

    Args:
        request (HttpRequest): Incoming HTTP request.
        pk (int): Primary key of the slot.

    Returns:
        HttpResponse: Confirmation page or redirect.

    Raises:
        Http404: If the slot does not exist.

    Examples:
        >>> response = slot_delete(request, 1)
        >>> response.status_code
        200
    """

    slot = get_object_or_404(WorkingSlot, pk=pk)
    if request.method == "POST":
        slot.delete()
        return redirect("masters:slot_list")
    return render(request, "masters/slot_confirm_delete.html", {"slot": slot})

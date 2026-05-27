"""Views for appointment booking workflow and dashboards."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AppointmentUpdateForm
from .models import Appointment


@login_required
def dashboard(request):
    """Display the client dashboard with upcoming appointments.

    Description:
        Provides an overview of the client's appointments and quick links
        to booking actions.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered dashboard page.

    Raises:
        None

    Examples:
        >>> response = dashboard(request)
        >>> response.status_code
        200
    """

    appointments = request.user.appointments.select_related(
        "master", "service", "slot"
    ).order_by("-created_at")
    return render(
        request,
        "appointments/dashboard.html",
        {"appointments": appointments},
    )


@login_required
def booking_step(request):
    """Display the multi-step booking form.

    Description:
        Allows clients to choose a service and time slot to create a booking.
        Slots are filtered to available ones only.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered booking page or redirect.

    Raises:
        None

    Examples:
        >>> response = booking_step(request)
        >>> response.status_code
        200
    """

    messages.info(request, "Запись теперь создается прямо в разделе услуг.")
    return redirect("services:list")


@login_required
def appointment_detail(request, pk):
    """Show appointment details for the client.

    Description:
        Displays appointment data and allows rescheduling or cancellation.

    Args:
        request (HttpRequest): Incoming HTTP request.
        pk (int): Appointment primary key.

    Returns:
        HttpResponse: Rendered appointment detail page.

    Raises:
        Http404: If the appointment does not exist.

    Examples:
        >>> response = appointment_detail(request, 1)
        >>> response.status_code
        200
    """

    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    return render(
        request,
        "appointments/appointment_detail.html",
        {"appointment": appointment},
    )


@login_required
def appointment_update(request, pk):
    """Reschedule an existing appointment.

    Description:
        Updates the slot for a booking and releases the old slot.

    Args:
        request (HttpRequest): Incoming HTTP request.
        pk (int): Appointment primary key.

    Returns:
        HttpResponse: Rendered update form or redirect.

    Raises:
        Http404: If the appointment does not exist.

    Examples:
        >>> response = appointment_update(request, 1)
        >>> response.status_code
        200
    """

    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    if appointment.status != Appointment.Status.PLANNED:
        messages.warning(request, "Перенос доступен только для запланированных записей.")
        return redirect("appointments:appointment_detail", pk=appointment.pk)

    old_slot = appointment.slot
    if request.method == "POST":
        form = AppointmentUpdateForm(request.POST, instance=appointment)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.master = updated.slot.master
            updated.save()
            old_slot.is_available = True
            old_slot.save(update_fields=["is_available"])
            updated.slot.is_available = False
            updated.slot.save(update_fields=["is_available"])
            messages.success(request, "Запись перенесена.")
            return redirect("appointments:appointment_detail", pk=appointment.pk)
    else:
        form = AppointmentUpdateForm(instance=appointment)
    return render(
        request,
        "appointments/appointment_form.html",
        {"form": form, "appointment": appointment},
    )


@login_required
def appointment_cancel(request, pk):
    """Cancel an appointment.

    Description:
        Marks the appointment as cancelled and releases the slot.

    Args:
        request (HttpRequest): Incoming HTTP request.
        pk (int): Appointment primary key.

    Returns:
        HttpResponse: Confirmation page or redirect.

    Raises:
        Http404: If the appointment does not exist.

    Examples:
        >>> response = appointment_cancel(request, 1)
        >>> response.status_code
        200
    """

    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    if appointment.status != Appointment.Status.PLANNED:
        messages.warning(request, "Эту запись уже нельзя отменить.")
        return redirect("appointments:appointment_detail", pk=appointment.pk)

    if request.method == "POST":
        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=["status"])
        appointment.slot.is_available = True
        appointment.slot.save(update_fields=["is_available"])
        messages.success(request, "Запись отменена.")
        return redirect("appointments:dashboard")
    return render(
        request,
        "appointments/appointment_confirm_cancel.html",
        {"appointment": appointment},
    )


@login_required
def admin_appointments(request):
    """Administrative list of all appointments.

    Description:
        Displays all bookings for administrators to review.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Rendered appointment list page.

    Raises:
        None

    Examples:
        >>> response = admin_appointments(request)
        >>> response.status_code
        200
    """

    appointments = Appointment.objects.select_related("client", "master", "service", "slot")
    return render(
        request,
        "appointments/admin_appointments.html",
        {"appointments": appointments},
    )

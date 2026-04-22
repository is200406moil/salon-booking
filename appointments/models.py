"""Appointment data models for the booking workflow."""

from django.conf import settings
from django.db import models

from masters.models import MasterProfile, WorkingSlot
from services.models import Service


class Appointment(models.Model):
    """Booking record for a client, service, and master.

    Description:
        Represents a confirmed booking created by a client for a selected
        service, master, and time slot. Includes status tracking for
        cancellation or rescheduling.

    Args:
        models.Model: Django base model class.

    Returns:
        Appointment: Persisted appointment instance.

    Raises:
        ValueError: Raised when booking data is inconsistent.

    Examples:
        >>> Appointment(client=user, master=profile, service=service)
        <Appointment: Клиент - Мастер - 2026-05-01 10:00>
    """

    class Status(models.TextChoices):
        """Booking status options."""

        PLANNED = "planned", "Запланирована"
        CANCELLED = "cancelled", "Отменена"
        COMPLETED = "completed", "Завершена"

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
        help_text="Клиент, записанный на услугу.",
    )
    master = models.ForeignKey(
        MasterProfile,
        on_delete=models.PROTECT,
        related_name="appointments",
        help_text="Мастер, оказывающий услугу.",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="appointments",
        help_text="Выбранная услуга.",
    )
    slot = models.OneToOneField(
        WorkingSlot,
        on_delete=models.PROTECT,
        related_name="appointment",
        help_text="Рабочий слот, выбранный для записи.",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
        help_text="Текущий статус записи.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Дата и время создания записи."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Дата и время последнего обновления."
    )
    notes = models.TextField(
        blank=True,
        help_text="Дополнительные пожелания или комментарии клиента.",
    )

    class Meta:
        """Model metadata for Appointment."""

        ordering = ["-created_at"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self) -> str:
        """Return a readable label for the appointment.

        Description:
            Combines client, master, and slot information for admin display.

        Args:
            None

        Returns:
            str: Human-readable appointment label.

        Raises:
            None

        Examples:
            >>> str(appointment)
            'Клиент - Мастер - 2026-05-01 10:00'
        """

        return (
            f"{self.client.get_full_name() or self.client.username} - "
            f"{self.master} - {self.slot.start_at:%Y-%m-%d %H:%M}"
        )

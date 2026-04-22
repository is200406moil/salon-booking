"""Data models describing salon services."""

from django.db import models


class Service(models.Model):
    """Service offered by the salon.

    Description:
        Represents a salon service with pricing, duration, and descriptive
        metadata. Services can be associated with masters and appointments.

    Args:
        models.Model: Django base model class.

    Returns:
        Service: Persisted service entity.

    Raises:
        ValueError: If duration or price values are invalid at runtime.

    Examples:
        >>> Service(name="Стрижка", price=1500, duration_minutes=60)
        <Service: Стрижка>
    """

    name = models.CharField(max_length=120, help_text="Название услуги.")
    description = models.TextField(help_text="Подробное описание услуги.")
    duration_minutes = models.PositiveIntegerField(
        help_text="Длительность услуги в минутах."
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Стоимость услуги в рублях.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Признак активности услуги для бронирования.",
    )

    class Meta:
        """Model metadata for Service."""

        ordering = ["name"]
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self) -> str:
        """Return a human-readable representation of the service.

        Description:
            Used in admin and templates to show the service name.

        Args:
            None

        Returns:
            str: Name of the service.

        Raises:
            None

        Examples:
            >>> str(Service(name="Маникюр"))
            'Маникюр'
        """

        return self.name

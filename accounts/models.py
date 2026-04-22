"""Database models for the accounts application."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role separation for salon participants.

    Description:
        Extends Django's :class:`~django.contrib.auth.models.AbstractUser` to add
        a ``role`` field and contact phone number. The role enables access
        control for client, master, and administrator workflows.

    Args:
        AbstractUser (models.Model): Base Django authentication user model.

    Returns:
        User: Instance of the customized user model.

    Raises:
        ValueError: Raised if an invalid role is assigned at runtime.

    Examples:
        >>> user = User(username="client1", role=User.Role.CLIENT)
        >>> user.is_client
        True
    """

    class Role(models.TextChoices):
        """Available user roles within the system."""

        CLIENT = "client", "Клиент"
        MASTER = "master", "Мастер"
        ADMIN = "admin", "Администратор"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
        help_text="Роль пользователя: клиент, мастер или администратор.",
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
        help_text="Контактный телефон пользователя для связи.",
    )

    @property
    def is_client(self) -> bool:
        """Check whether the user has the client role.

        Description:
            Used in templates and permission checks to verify the client role.

        Args:
            None

        Returns:
            bool: ``True`` when the user role is ``client``.

        Raises:
            None

        Examples:
            >>> User(role=User.Role.CLIENT).is_client
            True
        """

        return self.role == self.Role.CLIENT

    @property
    def is_master(self) -> bool:
        """Check whether the user has the master role.

        Description:
            Used in templates and permission checks to verify the master role.

        Args:
            None

        Returns:
            bool: ``True`` when the user role is ``master``.

        Raises:
            None

        Examples:
            >>> User(role=User.Role.MASTER).is_master
            True
        """

        return self.role == self.Role.MASTER

    @property
    def is_admin(self) -> bool:
        """Check whether the user has the administrator role.

        Description:
            Provides a clear role check in addition to ``is_staff``.

        Args:
            None

        Returns:
            bool: ``True`` when the user role is ``admin``.

        Raises:
            None

        Examples:
            >>> User(role=User.Role.ADMIN).is_admin
            True
        """

        return self.role == self.Role.ADMIN

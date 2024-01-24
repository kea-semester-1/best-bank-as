from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Overriding the default user model."""

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. "
        "A user will get all permissions granted to each of their groups.",
        related_name="custom_user_set",  # Unique related_name
        related_query_name="custom_user",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_user_set",  # Unique related_name
        related_query_name="custom_user",
    )

    @property
    def is_customer(self) -> bool:
        """Check if user is a customer."""
        return hasattr(self, "customer")

    @property
    def is_employee(self) -> bool:
        """Check if the user is an employee or a supervisor."""
        return self.groups.filter(name__in=["employee", "supervisor"]).exists()

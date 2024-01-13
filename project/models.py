from django.contrib.auth.models import AbstractUser
from django.db import models

from best_bank_as import enums


class CustomUser(AbstractUser):
    """Custom user model."""

    role = models.IntegerField(
        choices=enums.UserRole.choices,
        default=enums.UserRole.CUSTOMER,
        editable=True,
    )

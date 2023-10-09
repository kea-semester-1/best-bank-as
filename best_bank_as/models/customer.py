from django.contrib.auth.models import User
from django.db import models

from best_bank_as import enums
from best_bank_as.models.core import base_model


class Customer(base_model.BaseModel):
    """Model for customer."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    rank = models.IntegerField(
        choices=enums.CustomerRank.choices,
        default=2,
        editable=False,  # Should be programmatically set
    )

    def __str__(self) -> str:
        return f"ID: {self.pk}, Username: {self.user.username}, Rank: {self.rank}"

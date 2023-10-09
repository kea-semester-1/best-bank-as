from django.db import models

from best_bank_as import enums
from best_bank_as.models.core import base_model
from best_bank_as.models.customer import Customer


class Account(base_model.BaseModel):
    """Model for account."""

    account_number = models.IntegerField(
        unique=True,
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    type = models.IntegerField(
        choices=enums.AccountType.choices,
        default=0,
    )

    def __str__(self) -> str:
        """Return string representation of account."""
        return f"Account Number: {self.account_number}, Customer({self.customer})"

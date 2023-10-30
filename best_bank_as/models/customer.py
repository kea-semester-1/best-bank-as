from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet, Sum

from best_bank_as import enums
from best_bank_as.models.account import Account
from best_bank_as.models.core import base_model
from best_bank_as.models.ledger import Ledger


class Customer(base_model.BaseModel):
    """Model for customer."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    rank = models.IntegerField(
        choices=enums.CustomerRank.choices,
        default=2,
        editable=False,  # Should be programmatically set
    )
    status = models.IntegerField(
        choices=enums.CustomerStatus.choices,
        default=1,
        editable=False,  # Should be programmatically set
    )

    def get_accounts(self) -> QuerySet[Account]:
        """Retrieve all accounts for a give user."""
        accounts = Account.objects.filter(customer_id=self.pk)

        for account in accounts:
            balance = (
                Ledger.objects.filter(account_number_id=account.pk).aggregate(
                    Sum("amount")
                )["amount__sum"]
                or 0
            )
            account.balance = balance

        return accounts

    def __str__(self) -> str:
        return f"ID: {self.pk}, Username: {self.user.username}, Rank: {self.rank}"

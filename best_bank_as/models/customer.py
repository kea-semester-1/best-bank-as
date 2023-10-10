from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet, Sum

from best_bank_as.models.account import Account
from best_bank_as.models.core import base_model
from best_bank_as.models.customer_level import CustomerLevel
from best_bank_as.models.ledger import Ledger


class Customer(base_model.BaseModel):
    """Model for customer."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    customer_level = models.ForeignKey(CustomerLevel, on_delete=models.CASCADE)

    def get_accounts(self) -> QuerySet[Account]:
        """Retrieve all accounts for a give user."""
        accounts = Account.objects.filter(customer_id=self.pk)

        for account in accounts:
            balance = (
                Ledger.objects.filter(account_number_id=account.id).aggregate(
                    Sum("amount")
                )["amount__sum"]
                or 0
            )
            account.balance = -balance  # Reverse the sign of the balance

        return accounts


from django.contrib.auth.models import User
from django.db import models
from django.db.models import Prefetch, Q, QuerySet, Sum

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
        editable=True,  # Should be programmatically set
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
            account.balance = -balance  # Reverse the sign of the balance

        return accounts

    def update_status(self, status: enums.CustomerStatus) -> "Customer":
        """Method for updating status on the customer."""
        self.status = status
        self.save()
        return self

    @classmethod
    def search(cls, query: str) -> QuerySet["Customer"]:
        """Search for customers based on phone number, username, or account number."""
        return (
            cls.objects.filter(
                Q(phone_number__icontains=query)
                | Q(user__username__icontains=query)
                | Q(account__account_number__icontains=query)
            )
            .distinct()
            .select_related("user")
            .prefetch_related(Prefetch("account_set"))
        )

    @classmethod
    def get_pending(cls) -> QuerySet["Customer"]:
        """Get all pending customers."""
        return (
            cls.objects.filter(status=enums.CustomerStatus.PENDING)
            .select_related("user")
            .prefetch_related(Prefetch("account_set"))
        )

    def __str__(self) -> str:
        return f"ID: {self.pk}, Username: {self.user.username}, Rank: {self.rank}"

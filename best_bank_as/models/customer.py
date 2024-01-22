from typing import Any

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, QuerySet, Sum
from django.db.transaction import atomic

from best_bank_as import enums
from best_bank_as.models.account import Account
from best_bank_as.models.core.base_model import BaseModel
from best_bank_as.models.ledger import Ledger
from best_bank_as.models.loan import Loan
from best_bank_as.models.loan_application import LoanApplication


class Customer(BaseModel):
    """Model for customer."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    rank = models.IntegerField(
        choices=enums.CustomerRank.choices,
        default=2,
        editable=False,
    )
    status = models.IntegerField(
        choices=enums.CustomerStatus.choices,
        default=1,
        editable=True,
    )

    def get_accounts(self) -> QuerySet[Account]:
        """Retrieve all accounts for a give user."""
        accounts = Account.objects.filter(customer_id=self.pk)

        for account in accounts:
            balance = (
                Ledger.objects.filter(account=account).aggregate(Sum("amount"))[
                    "amount__sum"
                ]
                or 0
            )
            account.balance = balance

        return accounts

    def update_status(self, status: enums.CustomerStatus) -> "Customer":
        """Method for updating status on the customer."""
        self.status = status
        self.save()
        return self

    def update_rank(self, rank: int) -> None:
        """Method for updating rank on the customer."""
        self.rank = rank
        self.save()

    def set_customer_active_status(self) -> "Customer":
        """Set customer status.
        This will act as a solft delete.
        """
        self.user.is_active = not self.user.is_active
        self.user.save()
        return self

    def update_customer_fields(self, **kwargs: Any) -> "Customer":
        """Update customer fields."""
        for key, value in kwargs.items():
            if value is not None and value != "":
                if key == "phone_number":
                    setattr(self, key, value)
                else:
                    setattr(self.user, key, value)
        self.user.save()
        self.save()
        return self

    @atomic
    def create_loan(self, loan_application: LoanApplication) -> None:
        """Create a loan for the customer."""
        if not self.can_loan or not loan_application.approved:
            raise ValueError("Customer cannot create this loan.")

        loan_account = Account.objects.create(
            customer=self,
            account_type=enums.AccountType.LOAN,
            account_status=enums.AccountStatus.ACTIVE,
        )
        loan = Loan.objects.create(
            customer=self,
            loan_application=loan_application,
            loan_account=loan_account,
        )

        internal_account = Account.objects.get(
            account_type=enums.AccountType.INTERNAL, customer=None
        )

        Ledger.transfer(
            source_account=internal_account,
            destination_account=loan_account,
            amount=loan_application.amount,
        )
        loan.save()

    @property
    def can_loan(self) -> bool:
        """Check if customer can loan."""
        return self.rank >= enums.CustomerRank.BLUE

    @property
    def loan_applications(self) -> list[tuple[LoanApplication, str]]:
        """Get all loan applications for the customer."""
        return LoanApplication.filter_fmt(customer_id=self.pk)

    @classmethod
    def search(cls, query: str) -> QuerySet["Customer"]:
        """Search for customers based on phone number, username, or account number."""
        return (
            cls.objects.filter(
                Q(phone_number__icontains=query) | Q(user__username__icontains=query)
            )
            .distinct()
            .select_related("user")
            # .prefetch_related(Prefetch("account_set"))
        )

    @classmethod
    def get_pending(cls) -> QuerySet["Customer"]:
        """Get all pending customers."""
        return (
            cls.objects.filter(status=enums.CustomerStatus.PENDING).select_related(
                "user"
            )
            # .prefetch_related(Prefetch("account_set"))
        )

    def __str__(self) -> str:
        return f"ID: {self.pk}, Username: {self.user.username}, Rank: {self.rank}"

from decimal import Decimal
from typing import TYPE_CHECKING, Any

from django.db import models
from django.db.models import Sum

from best_bank_as import enums
from best_bank_as.enums import AccountStatus
from best_bank_as.models.core import base_model
from best_bank_as.models.ledger import Ledger

if TYPE_CHECKING:
    from best_bank_as.models.customer import Customer


class Account(base_model.BaseModel):
    """Model for account."""

    customer = models.ForeignKey(
        "best_bank_as.Customer", on_delete=models.CASCADE, null=True, blank=True
    )  # noqa: E501
    account_type = models.IntegerField(
        choices=enums.AccountType.choices,
        default=enums.AccountType.SAVINGS,
    )
    account_status = models.IntegerField(
        choices=enums.AccountStatus.choices, default=enums.AccountStatus.INACTIVE
    )  # noqa: E501

    @property
    def account_number(self) -> str:
        """Get account number."""
        return self.pk

    def get_balance(self) -> Decimal:
        """
        Retrieve the balance for the account.
        """
        balance = Ledger.objects.filter(account=self).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        return balance or Decimal(0)

    def get_transactions(self) -> list[dict[str, Any]]:
        """
        Retrieve all transactions related to the account.

        Returns:
        List of transactions with:
        - transaction_id: ID of the transaction
        - counterpart_account_number: Account number of the counterpart
        in the transaction # noqa: E501
        - amount: Amount involved in the transaction
        (positive if credit, negative if debit) # noqa: E501
        - date: Transaction date
        """

        # Fetch all transaction IDs related to this account.
        related_ledger_entries = (
            Ledger.objects.filter(account=self)
            .select_related("account_number", "transaction_id")
            .order_by("transaction_id_id", "created_at")
        )

        transactions = []

        for entry in related_ledger_entries:
            # Determine the counterpart entry (either source or destination)
            counterpart_entries = Ledger.objects.filter(
                transaction_id=entry.transaction_id
            ).exclude(account_number=self)

            for counterpart in counterpart_entries:
                transaction_data = {
                    "transaction_id": entry.transaction_id_id,
                    "counterpart_account_number": counterpart.account.account_number,  # noqa: E501
                    "amount": entry.amount,
                    "date": entry.created_at,
                }
                transactions.append(transaction_data)

        return transactions

    @classmethod
    def request_new_account(
        cls, customer: "Customer", status: enums.AccountStatus
    ) -> "Account":
        """Request a new account."""

        if status == AccountStatus.PENDING:
            has_pending_account = cls.objects.filter(
                customer=customer,
                account_status=AccountStatus.PENDING,
            ).exists()

            if has_pending_account:
                error = "You already have a pending account. Please wait for approval."
                raise ValueError(error)

        # Create a new account
        new_account = cls(customer=customer, account_status=status)
        new_account.save()
        return new_account

    def update_account_status(self, status_value: int) -> None:
        self.account_status = status_value
        self.save()

    def __str__(self) -> str:
        return f"Account Number: {self.account_number}, Customer({self.customer})"

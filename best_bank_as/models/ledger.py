from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models

from best_bank_as.enums import AccountStatus
from best_bank_as.models.core import base_model
from best_bank_as.models.transaction import Transaction

if TYPE_CHECKING:
    from best_bank_as.models.account import Account


class Ledger(base_model.BaseModel):
    """Model for ledger."""

    account = models.ForeignKey(
        "Account",
        on_delete=models.CASCADE,
        null=True,
    )
    transaction = models.ForeignKey(
        "Transaction",
        on_delete=models.CASCADE,
        null=True,
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    @classmethod
    def transfer(
        cls, source_account: "Account", destination_account: "Account", amount: Decimal
    ) -> None:
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")

        if source_account == destination_account:
            raise ValueError(
                "Source account and destination account cannot be the same."
            )

        if destination_account.account_status == AccountStatus.PENDING:
            raise ValueError("Cannot transfer money to pending account.")

        # TODO: Handle this with better error page and handling.
        if source_account.get_balance() < amount:
            raise ValueError("Amount cannot be less than balance")
        new_transaction = Transaction.objects.create()

        # Source account
        cls.objects.create(
            amount=-amount,
            account=source_account,
            transaction=new_transaction,
        )

        # Destination account
        cls.objects.create(
            amount=amount,
            account=destination_account,
            transaction=new_transaction,
        )

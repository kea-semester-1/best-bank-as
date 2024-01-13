from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models, transaction

from best_bank_as.db_models.core import base_model
from best_bank_as.db_models.transaction import Transaction
from best_bank_as.enums import AccountStatus

if TYPE_CHECKING:
    from best_bank_as.db_models.account import Account


class Ledger(base_model.BaseModel):
    """Model for ledger."""

    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    account_number = models.ForeignKey("best_bank_as.Account", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    @classmethod
    @transaction.atomic
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
            account_number=source_account,
            transaction_id=new_transaction,
        )

        # Destination account
        cls.objects.create(
            amount=amount,
            account_number=destination_account,
            transaction_id=new_transaction,
        )

from decimal import Decimal
from typing import Any

from django.db import models, transaction

from best_bank_as.enums import AccountStatus
from best_bank_as.models.core import base_model
from best_bank_as.models.transaction import Transaction
from best_bank_as import enums


class Ledger(base_model.BaseModel):
    """Model for ledger."""

    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    registration_number = models.ForeignKey(
        "best_bank_as.Bank", on_delete=models.CASCADE, default=1
    )
    account_number = models.ForeignKey("best_bank_as.Account", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(
        choices=enums.TransactionStatus.choices,
        default=0,
    )

    @classmethod
    @transaction.atomic
    def transfer(
        cls, source_account: Any, destination_account: Any, amount: Decimal
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

    @transaction.atomic
    def transfer_external(
        cls,
        source_account: Any,
        destination_reg_no: Any,
        destination_account: Any,
        amount: Decimal,
    ) -> None:
        if destination_account is None:
            raise ValueError("Registration number must be input")

        if amount <= 0:
            raise ValueError("Amount must be a positive number.")

        # TODO: Handle this with better error page and handling.
        if source_account.get_balance() < amount:
            raise ValueError("Amount cannot be less than balance")

        new_transaction = Transaction.objects.create()

        # Source account
        cls.objects.create(
            amount=-amount,
            reg_number=destination_reg_no,
            account_number=source_account,
            transaction_id=new_transaction,
            registration_number=destination_account,
            status=enums.TransactionStatus.PENDING,
        )

    @classmethod
    def enqueue_external_transfer() -> None:
        pass

    def set_status(cls, transaction_id: int, status: enums.TransactionStatus) -> None:
        ledger = cls.objects.filter(transaction_id=transaction_id)

        if ledger is None:
            raise ValueError("No ledger found")

        ledger.update(status=status)

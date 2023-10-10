from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from django.db import models
from django.db.models import Sum

from best_bank_as import enums
from best_bank_as.models.core import base_model
from best_bank_as.models.ledger import Ledger


class Account(base_model.BaseModel):
    """Model for account."""

    account_number = models.IntegerField(
        unique=True,
    )
    customer = models.ForeignKey("best_bank_as.Customer", on_delete=models.CASCADE)
    type = models.IntegerField(
        choices=enums.AccountType.choices,
        default=0,
    )

    def get_balance(self) -> Decimal:
        """
        Retrieve the balance for the account.
        """
        balance = Ledger.objects.filter(account_number_id=self.pk).aggregate(
            Sum("amount")
        )["amount__sum"]
        return balance or Decimal(0)

    def get_transactions(
        self,
    ) -> dict[int, list[dict[str, int | (datetime | Decimal)]]]:
        """
        Retrieve all transactions related to the account.
        """

        # Fetch all transaction IDs related to this account.
        related_transaction_ids = (
            Ledger.objects.filter(account_number_id=self.id)
            .values_list("transaction_id_id", flat=True)
            .distinct()
        )

        # Fetch all ledger entries that
        # are part of these transactions for the current account.
        current_account_movements = (
            Ledger.objects.filter(
                transaction_id_id__in=related_transaction_ids, account_number_id=self.id
            )
            .select_related("account_number")
            .order_by("transaction_id_id", "created_at")
            .values(
                "transaction_id_id",
                "amount",
                "created_at",
                "account_number",
            )
        )

        # Group the entries by transaction ID.
        transactions = defaultdict(list)
        for movement in current_account_movements:
            transactions[movement["transaction_id_id"]].append(movement)

        return dict(transactions)

    def __str__(self) -> str:
        return f"Account Number: {self.account_number}, Customer({self.customer})"

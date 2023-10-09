from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from django.db import models
from django.db.models import Sum

from best_bank_as.models.account_type import AccountType
from best_bank_as.models.core import base_model
from best_bank_as.models.ledger import Ledger


class Account(base_model.BaseModel):
    """Model for account."""

    account_number = models.IntegerField(unique=True)
    customer = models.ForeignKey("best_bank_as.Customer", on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True)

    def get_balance(self) -> Decimal:
        """
        Retrieve the balance for the account.
        """
        balance = Ledger.objects.filter(account_number_id=self.id).aggregate(
            Sum("amount")
        )["amount__sum"]
        return balance

    def get_transactions(
        self,
    ) -> dict[int, list[dict[str, int | (datetime | Decimal)]]]:
        """
        Retrieve all transactions related to the account.
        """

        # First, fetch all transaction IDs related to this account.
        related_transaction_ids = (
            Ledger.objects.filter(account_number_id=self.id)
            .values_list("transaction_id_id", flat=True)
            .distinct()
        )

        # Fetch all ledger entries that are part of these transactions
        # excluding the current account's entries.
        counterpart_movements = (
            Ledger.objects.filter(transaction_id_id__in=related_transaction_ids)
            .exclude(account_number_id=self.id)
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
        for movement in counterpart_movements:
            transactions[movement["transaction_id_id"]].append(movement)

        return dict(transactions)

    def __str__(self):
        return str(self.account_number)

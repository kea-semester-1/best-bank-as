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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    type = models.IntegerField(
        choices=enums.AccountType.choices,
        default=0,
    )

    def get_balance(self) -> Decimal:
        """
        Retrieve the balance for the account.
        """
        balance = Ledger.objects.filter(account_number_id=self.id).aggregate(
            Sum("amount")
        )["amount__sum"] or Decimal(0)
        return -balance

    def get_transactions(
        self,
    ) -> dict[int, list[dict[str, int | (datetime | Decimal)]]]:
        """
        Retrieve all transactions related to the account.
        """

        movements = (
            Ledger.objects.filter(account_number_id=self.id)
            .select_related("account_number")
            .order_by("transaction_id_id", "created_at")
        )

        transactions = defaultdict(list)

        # Loop over each movement.
        for movement in movements:
            # Retrieve the counterpart movements for each transaction.
            counterpart_movements = (
                Ledger.objects.filter(transaction_id_id=movement.transaction_id_id)
                .exclude(account_number_id=self.id)
                .select_related("account_number")
            )

            # Loop over each counterpart movement
            # and append it to the transactions' dictionary.
            for counterpart in counterpart_movements:
                transactions[movement.transaction_id_id].append(
                    {
                        "amount": counterpart.amount,
                        "created_at": counterpart.created_at,
                        "account_number": counterpart.account_number.account_number,
                    }
                )

        return dict(transactions)

    def __str__(self) -> str:
        """Return string representation of account."""
        return f"Account Number: {self.account_number}, Customer({self.customer})"

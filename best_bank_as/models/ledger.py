from django.db import models

from best_bank_as.models.core import base_model
from best_bank_as.models.transaction import Transaction


class Ledger(base_model.BaseModel):
    """Model for ledger."""

    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    account_number = models.ForeignKey("best_bank_as.account", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

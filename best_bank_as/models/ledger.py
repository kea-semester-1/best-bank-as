from django.db import models

from best_bank_as.models.account import Account
from best_bank_as.models.transaction import Transaction


class Ledger(models.Model):
    """Model for ledger."""

    ledger_id = models.AutoField(primary_key=True)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

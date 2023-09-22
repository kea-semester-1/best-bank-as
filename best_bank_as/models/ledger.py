from django.db import models
from best_bank_as.models.account import Account
from best_bank_as.models.transaction_table import TransactionTable


class Ledger(models.Model):
    transaction = models.ForeignKey(TransactionTable, on_delete=models.CASCADE)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
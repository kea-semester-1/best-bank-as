from django.db import models

from best_bank_as.models.account_type import AccountType
from best_bank_as.models.customer import Customer


class Account(models.Model):
    """Model for account"""

    account_id = models.AutoField(primary_key=True)
    account_number = models.IntegerField(unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

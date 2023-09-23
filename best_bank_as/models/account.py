from django.db import models
from best_bank_as.models.customer import Customer
from best_bank_as.models.account_type import AccountType
from best_bank_as.models.core import base_model


class Account(base_model.BaseModel):
    """Model for account"""

    account_number = models.IntegerField(unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True)

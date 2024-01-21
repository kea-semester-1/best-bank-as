from django.db import models
from best_bank_as.models.core import base_model


class Bank(base_model.BaseModel):
    """
    Model for banks.
    This will store all banks available for bank to bank transfer.
    """

    reg_number = models.CharField(unique=True, max_length=4)
    bank_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

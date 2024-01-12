from django.db import models

from best_bank_as.db_models.core import base_model


class AccountType(base_model.BaseModel):
    """Model for account_type."""

    account_type_name = models.CharField(max_length=255)

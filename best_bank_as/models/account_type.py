from django.db import models


class AccountType(models.Model):
    """Model for account_type."""

    account_type_id = models.AutoField(primary_key=True)
    account_type_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

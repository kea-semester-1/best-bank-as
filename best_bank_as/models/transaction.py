from django.db import models


class Transaction(models.Model):
    """Model for transactions."""

    transaction_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

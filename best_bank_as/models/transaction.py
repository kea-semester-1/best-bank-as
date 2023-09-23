from django.db import models


class Transaction(models.Model):
    """Model for transactions"""

    transaction_id = models.AutoField(primary_key=True)

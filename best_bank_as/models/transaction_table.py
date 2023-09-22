from django.db import models

class TransactionTable(models.Model):
    transaction_id = models.AutoField(primary_key=True)
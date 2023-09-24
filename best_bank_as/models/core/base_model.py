from django.db import models


class BaseModel(models.Model):
    """Model for account_type."""

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

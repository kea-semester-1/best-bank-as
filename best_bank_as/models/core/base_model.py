
from django.db import models


class BaseModel(models.Model):
    """Model for account_type."""

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

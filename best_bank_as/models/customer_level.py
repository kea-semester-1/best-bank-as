from django.db import models

from best_bank_as.models.core import base_model


class CustomerLevel(base_model.BaseModel):
    """Model for customer_level."""

    customer_level_name = models.CharField(max_length=255)

from django.contrib.auth.models import User
from django.db import models

from best_bank_as.models.core import base_model
from best_bank_as.models.customer_level import CustomerLevel


class Customer(base_model.BaseModel):
    """Model for customer."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    customer_level = models.ForeignKey(CustomerLevel, on_delete=models.CASCADE)

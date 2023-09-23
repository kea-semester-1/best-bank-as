from django.db import models
from django.contrib.auth.models import User
from best_bank_as.models.customer_level import CustomerLevel


class Customer(models.Model):
    """Model for customer."""

    customer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    customer_level = models.ForeignKey(CustomerLevel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

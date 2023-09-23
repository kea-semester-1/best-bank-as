from django.db import models


class CustomerLevel(models.Model):
    """Model for customer_level."""

    customer_level_id = models.AutoField(primary_key=True)
    customer_level_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

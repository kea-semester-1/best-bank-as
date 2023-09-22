from django.db import models

class CustomerLevel(models.Model):
    customer_level_id = models.AutoField(primary_key=True)
    customer_level_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
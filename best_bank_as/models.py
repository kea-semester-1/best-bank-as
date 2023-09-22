from enum import Enum

from django.db import models
from django.contrib.auth.models import User

class CustomerLevel(models.Model):
    customer_level_id = models.AutoField(primary_key=True)
    customer_level_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    customer_level = models.ForeignKey(CustomerLevel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
class AccountType(models.Model):
    account_type_id = models.AutoField(primary_key=True)
    account_type_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_number = models.IntegerField(unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class TransactionTable(models.Model):
    transaction_id = models.AutoField(primary_key=True)

class Ledger(models.Model):
    transaction = models.ForeignKey(TransactionTable, on_delete=models.CASCADE)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
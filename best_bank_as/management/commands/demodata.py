import random
import secrets
from decimal import Decimal
from typing import Any

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from best_bank_as.models.account import Account
from best_bank_as.models.customer import Customer
from best_bank_as.models.ledger import Ledger
from best_bank_as.models.transaction import Transaction


class Command(BaseCommand):
	@transaction.atomic
	def handle(self, **options):
		print("Adding demo data...")
		
		bank = User.objects.create_user(username="bank", email="", password=secrets.token_urlsafe(64))
		bank.save()
		bank_customer = Customer.objects.create(user=bank, phone_number="11223344")
		bank_customer.save()
		
		bank_account_number = 1
		bank_account = Account.objects.create(account_number=bank_account_number, customer=bank_customer)
		Ledger.objects.create(transaction_id=Transaction.objects.create(), account_number=bank_account, amount=10000000)
		
		user1 = User.objects.create_user(username="Malthe", email="", password="123")
		user2 = User.objects.create_user(username="Mohammed", email="", password="123")
		user3 = User.objects.create_user(username="Martin", email="", password="123")
		
		user1.save()
		user2.save()
		user3.save()
		
		customer1 = Customer.objects.create(user=user1, phone_number="11223344")
		customer2 = Customer.objects.create(user=user2, phone_number="11223344")
		customer3 = Customer.objects.create(user=user3, phone_number="11223344")
		
		customer1.save()
		customer2.save()
		customer3.save()
		
	
		account1 = Account.objects.create(account_number=2, customer=customer1)
		account2 = Account.objects.create(account_number=3, customer=customer1)
		account1.save()
		account2.save()
		
		account3 = Account.objects.create(account_number=4, customer=customer2)
		account4 = Account.objects.create(account_number=5, customer=customer2)
		account3.save()
		account4.save()
		
		account5 = Account.objects.create(account_number=6, customer=customer3)
		account6 = Account.objects.create(account_number=7, customer=customer3)
		account5.save()
		account6.save()
		
		Ledger.transfer(source_account=bank_account, destination_account=account1, amount=Decimal(value=5000))
		Ledger.transfer(source_account=bank_account, destination_account=account3, amount=Decimal(value=5000))
		Ledger.transfer(source_account=bank_account, destination_account=account5, amount=Decimal(value=5000))
		
		print("Demo data inserted.")
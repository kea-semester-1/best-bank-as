from decimal import Decimal
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from best_bank_as import enums
from best_bank_as.db_models.account import Account
from best_bank_as.db_models.customer import Customer
from best_bank_as.db_models.ledger import Ledger

User = get_user_model()


class Command(BaseCommand):
    """Inserting demo data."""

    @atomic
    def handle(self, **options: Any) -> None:
        """Inserting demo data."""
        print("Adding demo data...")

        user1 = User.objects.create_user(username="Malthe", email="", password="123")
        user2 = User.objects.create_user(username="Mo", email="", password="123")
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

        account1 = Account.objects.create(
            customer=customer1,
            account_status=enums.AccountStatus.ACTIVE,
        )
        account2 = Account.objects.create(
            customer=customer1, account_status=enums.AccountStatus.ACTIVE
        )
        account1.save()
        account2.save()

        account3 = Account.objects.create(
            customer=customer2, account_status=enums.AccountStatus.ACTIVE
        )
        account4 = Account.objects.create(
            customer=customer2, account_status=enums.AccountStatus.ACTIVE
        )
        account3.save()
        account4.save()

        account5 = Account.objects.create(
            customer=customer3, account_status=enums.AccountStatus.ACTIVE
        )
        account6 = Account.objects.create(
            customer=customer3, account_status=enums.AccountStatus.ACTIVE
        )
        account5.save()
        account6.save()

        bank_account = Account.objects.filter(pk=1)

        Ledger.transfer(
            source_account=bank_account[0],
            destination_account=account1,
            amount=Decimal(value=5000),
        )
        Ledger.transfer(
            source_account=bank_account[0],
            destination_account=account3,
            amount=Decimal(value=5000),
        )
        Ledger.transfer(
            source_account=bank_account[0],
            destination_account=account5,
            amount=Decimal(value=5000),
        )

        print("Demo data inserted.")

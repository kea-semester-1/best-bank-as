import secrets
from typing import Any

from django.core.management.base import BaseCommand

from best_bank_as import enums
from best_bank_as.models.account_type import AccountType
from best_bank_as.models.bank import Bank
from best_bank_as.models.account import Account
from best_bank_as.models.customer import Customer
from best_bank_as.models.ledger import Ledger
from best_bank_as.models.transaction import Transaction
from django.contrib.auth.models import User


class Command(BaseCommand):
    """Command for provisioning."""

    def handle(self, **options: Any) -> None:
        """Handle command."""
        print("Provisioning...")
        if not AccountType.objects.all():
            AccountType.objects.create(
                account_type_name=enums.AccountType.choices[0][1]
            )
            AccountType.objects.create(
                account_type_name=enums.AccountType.choices[1][1]
            )
            AccountType.objects.create(
                account_type_name=enums.AccountType.choices[2][1]
            )

        if not Bank.objects.all():
            Bank.objects.create(
                reg_number="6666",
                bank_name="Malthe Bank",
                branch_name="Malthe branch",
                url="api_url",
            )
            Bank.objects.create(
                reg_number="6969",
                bank_name="Martin Bank",
                branch_name="Marin branch",
                url="api_url",
            )

            Bank.objects.create(
                reg_number="0420",
                bank_name="Mo Bank",
                branch_name="Mo branch",
                url="api_url",
            )

        bank = User.objects.create_user(
            username="bank", email="", password=secrets.token_urlsafe(64)
        )
        bank.save()
        bank_customer = Customer.objects.create(user=bank, phone_number="11223344")
        bank_customer.save()

        bank_account_number = 1
        bank_account = Account.objects.create(
            account_number=bank_account_number, customer=bank_customer
        )
        Ledger.objects.create(
            transaction_id=Transaction.objects.create(),
            account_number=bank_account,
            registration_number_id=1,
            amount=10000000,
        )
        if not Account.objects.all():
            Account.objects.create()

        print("Provision completed.")

import secrets
from typing import Any

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from best_bank_as import enums
from best_bank_as.db_models.account import Account
from best_bank_as.db_models.bank import Bank
from best_bank_as.db_models.customer import Customer
from best_bank_as.db_models.ledger import Ledger
from best_bank_as.db_models.transaction import Transaction
from best_bank_as.models import CustomUser


def create_groups() -> None:
    """Create groups, and assign permissions to them."""

    base_permissions = [
        "view_account",
        "view_customer",
        "view_ledger",
        "view_loanapplication",
        "view_loan",
        "view_transaction",
    ]

    customer_permissions = base_permissions + [
        "add_account",
        "add_ledger",
        "add_loanapplication",
        "add_transaction",
        "change_account",
    ]

    employee_permissions = customer_permissions + [
        "add_customer",
        "change_customer",
        "change_ledger",
        "change_loanapplication",
        "change_loan",
        "change_transaction",
    ]

    supervisor_permissions = employee_permissions + ["add_loan", "change_loan"]

    customer_permissions.append("delete_loanapplication")

    permission_mapping = {
        "customer": customer_permissions,
        "employee": employee_permissions,
        "supervisor": supervisor_permissions,
    }

    for group_name, permissions in permission_mapping.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                print(f"Permission with codename '{perm}' not found.")


@atomic
def create_internal_bank_account() -> Account:
    """Create internal bank account."""
    account = Account.objects.create(
        account_type=enums.AccountType.INTERNAL,
        account_status=enums.AccountStatus.ACTIVE,
        customer=None,
    )

    transaction = Transaction.objects.create()

    # Add starting balance
    Ledger.objects.create(
        account=account,
        transaction=transaction,
        amount=1000000,
    )

    return account


class Command(BaseCommand):
    """Command for provisioning."""

    def handle(self, **options: Any) -> None:
        """Handle command."""
        print("Provisioning...")

        if not Bank.objects.all():
            Bank.objects.create(
                reg_number="6666",
                bank_name="Malthe Bank",
                branch_name="Malthe branch",
                url="https://malthegram.dk",
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
                url="https://www.what-lol.dk",
            )

        bank = CustomUser.objects.create_user(
            username="bank", email="", password=secrets.token_urlsafe(64)
        )
        bank.save()
        bank_customer = Customer.objects.create(user=bank, phone_number="11223344")
        bank_customer.save()

        if not Account.objects.filter(account_type=enums.AccountType.INTERNAL).exists():
            print("Creating internal bank account...")
            create_internal_bank_account()

        if not Account.objects.all():
            Account.objects.create()

        if not Group.objects.all():
            print("Creating groups...")
            create_groups()
        else:
            print("Groups already created.")

        print("Provision completed.")

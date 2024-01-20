from typing import Any

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from best_bank_as import enums
from best_bank_as.models.account_type import AccountType


def create_groups() -> None:
    """Create groups, and assign permissions to them."""

    base_permissions = [
        "view_account",
        "view_accounttype",
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
        "add_accounttype",
        "add_customer",
        "change_accounttype",
        "change_customer",
        "change_ledger",
        "change_loanapplication",
        "change_loan",
        "change_transaction",
    ]

    supervisor_permissions = employee_permissions + ["add_loan", "change_loan"]

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

        if not Group.objects.all():
            print("Creating groups...")
            create_groups()
        else:
            print("Groups already created.")

        print("Provision completed.")

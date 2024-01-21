from typing import Any

from django.core.management.base import BaseCommand

from best_bank_as import enums
from best_bank_as.models.account_type import AccountType
from best_bank_as.models.bank import Bank


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
                reg_number="4200",
                bank_name="Martin Bank",
                branch_name="Marin branch",
                url="api_url",
            )

            Bank.objects.create(
                reg_number="6969",
                bank_name="Mo Bank",
                branch_name="Mo branch",
                url="api_url",
            )

        print("Provision completed.")

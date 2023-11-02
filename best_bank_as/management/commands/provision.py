from typing import Any

from django.core.management.base import BaseCommand

from best_bank_as import enums
from best_bank_as.models.account_type import AccountType


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

        print("Provision completed.")

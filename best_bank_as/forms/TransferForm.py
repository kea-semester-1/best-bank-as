from typing import Any

from django import forms
from django.contrib.auth.models import User

from best_bank_as.enums import AccountStatus
from best_bank_as.models.account import Account


class TransferForm(forms.Form):
    """Form for transferring money."""

    source_account = forms.ModelChoiceField(
        queryset=Account.objects.none(), label="Source Account"
    )

    registration_number = forms.CharField(label="Destination Registration Number")
    destination_account = forms.IntegerField(label="Destination Account Number")
    amount = forms.DecimalField(decimal_places=2, label="Amount to Transfer")

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["source_account"].queryset = Account.objects.filter(
            customer=user.customer, account_status=AccountStatus.ACTIVE
        )


class TransferFormExternal(TransferForm):
    destination_reg_no: int

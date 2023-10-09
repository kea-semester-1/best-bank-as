from django import forms

from best_bank_as.models.account import Account


class TransferForm(forms.Form):
    source_account = forms.ModelChoiceField(
        queryset=Account.objects.none(), label="Source Account"
    )

    destination_account = forms.IntegerField(label="Destination Account Number")
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2, label="Amount to Transfer"
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["source_account"].queryset = Account.objects.filter(
            customer=user.customer
        )

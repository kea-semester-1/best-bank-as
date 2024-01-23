from django import forms


class ExternalTransferForm(forms.Form):
    destination_account = forms.IntegerField()
    amount = forms.DecimalField(decimal_places=2)
    registration_number = forms.CharField()

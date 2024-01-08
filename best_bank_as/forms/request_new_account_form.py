from django import forms


class NewAccountRequestForm(forms.Form):
    """Form to request a new account.
    No fields needed since we're only signaling an intent."""

    pass

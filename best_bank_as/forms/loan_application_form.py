from typing import Any

from django import forms


class LoanApplicationForm(forms.Form):
    """Form for loan application."""

    def __init__(self, *args: Any, **kwargs: Any):
        """Override init to pass in customer."""
        self.customer = kwargs.pop("customer")
        super().__init__(*args, **kwargs)

    reason = forms.CharField(label="Reason", max_length=255)
    amount = forms.DecimalField(label="Amount", max_digits=10, decimal_places=2)

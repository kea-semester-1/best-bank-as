from django import forms

from best_bank_as.db_models.customer import Customer
from best_bank_as.models import CustomUser


class UserCreationForm(forms.ModelForm):
    """User form."""

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ["username", "password"]


class CustomerCreationForm(forms.ModelForm):
    """Customer form."""

    class Meta:
        model = Customer
        fields = ["phone_number"]


class CustomerApproveForm(forms.ModelForm):
    """Customer form."""

    class Meta:
        model = Customer
        fields = ["status"]

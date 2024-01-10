from django import forms
from django.contrib.auth.models import User

from best_bank_as.models.customer import Customer


class UserCreationForm(forms.ModelForm):
    """User form."""

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
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


class UserCreationByEmployeeForm(forms.ModelForm):
    """User form when employee creates a user."""

    class Meta:
        model = User
        fields = ["username"]
        exclude = ("password",)

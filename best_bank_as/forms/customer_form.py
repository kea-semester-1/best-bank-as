from typing import Any
from django import forms
from django.contrib.auth.models import User

from best_bank_as.models.customer import Customer


class UserCreationForm(forms.ModelForm):
    """User form."""

    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def __init__(self, *args, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs: Any)
        self.fields["username"].widget.attrs["placeholder"] = "BestCustomer34"
        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["email"].widget.attrs["placeholder"] = "customer@best_bank_as.com"
        self.fields["password"].widget.attrs["placeholder"] = "******"


class CustomerCreationForm(forms.ModelForm):
    """Customer form."""

    phone_number = forms.CharField(widget=forms.NumberInput())

    class Meta:
        model = Customer
        fields = ["phone_number"]

    def __init__(self, *args, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs: Any)
        self.fields["phone_number"].widget.attrs["placeholder"] = "11223344"


class CustomerApproveForm(forms.ModelForm):
    """Customer form."""

    class Meta:
        model = Customer
        fields = ["status"]


class UserCreationByEmployeeForm(UserCreationForm):
    """User form when employee creates a user."""

    class Meta(UserCreationForm.Meta):
        exclude = ("password",)

    def __init__(self, *args, **kwargs: Any) -> None:
        """Init method."""
        super().__init__(*args, **kwargs: Any)
        # Since 'password' field is excluded, we remove it from the fields
        if "password" in self.fields:
            self.fields.pop("password")


class UserUpdateForm(UserCreationForm):
    """Form for updating a user instance."""

    class Meta(UserCreationForm.Meta):
        exclude = ("password",)

    def __init__(self, *args, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs: Any)
        for field in self.fields.values():
            field.required = False

        if "password" in self.fields:
            self.fields.pop("password")


class CustomerUpdateForm(CustomerCreationForm):
    """Form for updating a customer instance."""

    class Meta(CustomerCreationForm.Meta):
        pass

    def __init__(self, *args, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs: Any)
        self.fields["phone_number"].required = False

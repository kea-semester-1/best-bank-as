from django.shortcuts import render, redirect
from django.views import View
from best_bank_as.forms.customer_form import CustomerCreationForm, UserCreationForm
from best_bank_as.enums import CustomerStatus
from django.http import HttpRequest, HttpResponse


class CustomerCreateView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        user_form = UserCreationForm()
        customer_form = CustomerCreationForm()
        return render(
            request,
            "registration/register_customer.html",
            {"user_form": user_form, "customer_form": customer_form},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        user_form = UserCreationForm(request.POST)
        customer_form = CustomerCreationForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            # Create User instance
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.status = CustomerStatus.PENDING
            new_user.save()

            # Create Customer instance
            new_customer = customer_form.save(commit=False)
            new_customer.user = new_user
            new_customer.save()

            return redirect("login")

        return render(
            request,
            "registration/register_customer.html",
            {"user_form": user_form, "customer_form": customer_form},
        )


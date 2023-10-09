from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from best_bank_as.enums import ApplicationStatus, ApplicationType
from best_bank_as.forms.loan_application_form import LoanApplicationForm
from best_bank_as.models.account import Account
from best_bank_as.models.customer import Customer
from best_bank_as.models.customer_application import CustomerApplication
from best_bank_as.models.ledger import Ledger


def index(request: HttpRequest) -> HttpResponse:
    """View for index."""

    return render(request, "best_bank_as/index.html")


@login_required
def profile_page(request: HttpRequest, username: str) -> HttpResponse:
    """View for a user's profile page."""
    user = get_object_or_404(User, username=username)

    customer = get_object_or_404(Customer, user=user)

    if request.user != user:
        return HttpResponseForbidden(
            render(request, "best_bank_as/error_pages/error_page.html")
        )

    context = {"customer": customer}

    return render(request, "best_bank_as/profile.html", context)


@login_required
def get_accounts(request: HttpRequest, pk: int) -> HttpResponse:
    """Retrieve all accounts for a given user."""
    user = get_object_or_404(User, pk=pk)
    customer = get_object_or_404(Customer, user=user)

    accounts = customer.get_accounts()

    context = {"accounts": accounts}
    return render(request, "best_bank_as/accounts/accounts.html", context)


@login_required
def get_details(request: HttpRequest, pk: int) -> HttpResponse:
    """Retrieve information for a given account."""

    account = get_object_or_404(Account, pk=pk)

    balance = account.get_balance()
    transactions = account.get_transactions()

    context = {"account": account, "balance": balance, "transactions": transactions}

    return render(request, "best_bank_as/accounts/details.html", context)


@login_required
def loans_page(request: HttpRequest) -> HttpResponse:
    """Loans page view."""
    user = request.user
    customer = get_object_or_404(Customer, user=user)

    loan_applications = CustomerApplication.objects.filter(
        customer_id=customer.pk, type=ApplicationType.LOAN
    )
    statuses = [
        ApplicationStatus.int_to_enum(application.status)
        for application in loan_applications
    ]

    context = {
        "customer": customer,
        "loan_applications": zip(loan_applications, statuses, strict=True),
    }

    # if customer.rank <= CustomerRank.BLUE:
    #     return render(request, "best_bank_as/loans/loans.html", context)

    if request.method != "POST":
        context["form"] = LoanApplicationForm(customer=customer)
        return render(request, "best_bank_as/loans/loans.html", context)

    form = LoanApplicationForm(data=request.POST, customer=customer)
    if not form.is_valid():
        return render(
            request,
            "best_bank_as/error_pages/error_page.html",
        )
    context["form"] = form

    form_data = form.cleaned_data
    reason = form_data["reason"]
    amount = form_data["amount"]

    application = CustomerApplication(
        reason=reason,
        amount=amount,
        type=ApplicationType.LOAN,
        status=ApplicationStatus.PENDING,
        customer=customer,
    )
    application.save()

    return render(request, "best_bank_as/loans/loans.html", context)


@login_required
def delete_loan_application(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete a loan application."""
    application = get_object_or_404(CustomerApplication, pk=pk)
    application.delete()

    return redirect("loans-page")

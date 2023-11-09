from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from best_bank_as.enums import (
    ApplicationStatus,
    ApplicationType,
    CustomerRank,
    CustomerStatus,
)

from best_bank_as.forms.loan_application_form import LoanApplicationForm
from best_bank_as.forms.TransferForm import TransferForm
from best_bank_as.models.account import Account
from best_bank_as.models.customer import Customer
from best_bank_as.models.customer_application import CustomerApplication
from best_bank_as.models.ledger import Ledger


def index(request: HttpRequest) -> HttpResponse:
    """View for index."""

    return render(request, "best_bank_as/index.html")


# TODO: Is this the correct way to ensure user can only see his own page
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
def get_accounts_list(request: HttpRequest) -> HttpResponse:  # TODO: FIX LOGIC
    """Retrieve all accounts for a given user."""

    customer = get_object_or_404(Customer, user=request.user)

    accounts = customer.get_accounts()

    context = {"accounts": accounts}
    return render(request, "best_bank_as/accounts/account_list.html", context)


@login_required
def get_account_details(request: HttpRequest, pk: int) -> HttpResponse:
    """Retrieve information for a given account."""
    account = get_object_or_404(Account, pk=pk)

    if request.user != account.customer.user:
        return HttpResponseForbidden(
            render(request, "best_bank_as/error_pages/error_page.html")
        )

    if request.method == "GET":
        balance = account.get_balance()
        transactions = account.get_transactions()

    if request.method == "POST":
        ...

    if request.method == "PUT":
        ...

    if request.method == "DELETE":  # TODO: Soft delete
        ...

    context = {"account": account, "balance": balance, "transactions": transactions}

    return render(request, "best_bank_as/accounts/account_details.html", context)


@login_required
def staff_page(request: HttpRequest, username: str) -> HttpResponse:
    """View for a staff page."""
    user = get_object_or_404(User, username=username)

    if request.user != user:
        return HttpResponseForbidden(
            render(request, "best_bank_as/error_pages/error_page.html")
        )
    context = {user: user}

    return render(request, "best_bank_as/staff.html", context)


@login_required
def search_customer(request: HttpRequest) -> HttpResponse:
    """View for searching customers."""
    query = request.GET.get("query", "")

    if not request.user.is_staff:
        return HttpResponseForbidden()

    customers = Customer.search(query=query)

    context = {"customers": customers, "query": query}
    return render(request, "best_bank_as/customers/customers_search.html", context)


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

    if customer.rank <= CustomerRank.BLUE:
        return render(request, "best_bank_as/loans/loans.html", context)

    if request.method != "POST":
        context["form"] = LoanApplicationForm(customer=customer)
        return render(request, "best_bank_as/loans/loans.html", context)

    form = LoanApplicationForm(data=request.POST, customer=customer)
    if not form.is_valid():
        return render(
            request,
            "best_bank_as/error_pages/error_page.html",
        )

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

    return redirect("best_bank_as:loan_application_list.html")


@login_required()
def transfer_money(request: HttpRequest) -> HttpResponse:
    """View to transfer money from account to account."""
    if request.method != "POST":
        return render(
            request,
            "best_bank_as/handle_funds/transfer-money.html",
            {"form": TransferForm(user=request.user)},
        )
    form = TransferForm(data=request.POST, user=request.user)
    if not form.is_valid():  # or throw exception
        return render(
            request,
            "best_bank_as/handle_funds/transfer-money.html",
            {"form": form},
        )
    source_account = form.cleaned_data["source_account"]
    destination_account = form.cleaned_data["destination_account"]
    destination_account_instance = Account.objects.get(
        account_number=destination_account
    )
    amount = form.cleaned_data["amount"]
    Ledger.transfer(source_account, destination_account_instance, amount)
    return redirect("best_bank_as:index")

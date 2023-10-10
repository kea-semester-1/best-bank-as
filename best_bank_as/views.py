from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Prefetch
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from best_bank_as.models.account import Account
from best_bank_as.models.customer import Customer


def index(request: HttpRequest) -> HttpResponse:
    """View for index."""

    return render(request, "best_bank_as/index.html")


@login_required
def profile_page(request: HttpRequest, username: str) -> HttpResponse:
    """View for a user's profile page."""
    user = get_object_or_404(User, username=username)

    if request.user != user:
        return HttpResponseForbidden(
            render(request, "best_bank_as/error_pages/error_page.html")
        )
    context = {user: user}

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
def get_customers(request: HttpRequest) -> HttpResponse:
    """Retrieve all customer in the bank."""

    if not request.user.is_staff:
        return HttpResponseForbidden()

    customers = Customer.objects.all()
    context = {"customers": customers}
    return render(request, "best_bank_as/customers/customers.html", context)


@login_required
def search_customer(request: HttpRequest) -> HttpResponse:
    """View for searching customers"""
    query = request.GET.get("query", "")

    if not request.user.is_staff:
        return HttpResponseForbidden()

    # Using select_related and prefetch_related to optimize queries
    customers = (
        Customer.objects.filter(
            Q(phone_number__icontains=query) | Q(user__username__icontains=query)
        )
        .select_related("user", "customer_level")
        .prefetch_related(
            Prefetch(
                "account_set", queryset=Account.objects.select_related("account_type")
            )
        )
    )

    context = {"customers": customers, "query": query}
    return render(request, "best_bank_as/customers/search_results.html", context)

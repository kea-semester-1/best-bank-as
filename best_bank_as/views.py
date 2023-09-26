from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from best_bank_as.models.account import Account
from best_bank_as.models.ledger import Ledger


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

    accounts = Account.objects.filter(customer_id=user.pk)

    for account in accounts:
        balance = (
            Ledger.objects.filter(account_number_id=account.id).aggregate(
                Sum("amount")
            )["amount__sum"]
            or 0
        )
        account.balance = -balance  # Reverse the sign of the balance

    context = {"accounts": accounts}
    return render(request, "best_bank_as/accounts/accounts.html", context)


@login_required
def get_details(request: HttpRequest, pk: int) -> HttpResponse:
    """Retrieve information for a given account."""
    account = get_object_or_404(Account, pk=pk)

    balance = (
        Ledger.objects.filter(account_number_id=account.id).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    account.balance = -balance
    # Find all movements for the given account
    movements = (
        Ledger.objects.filter(account_number_id=pk)
        .select_related("account_number")
        .order_by("transaction_id_id", "created_at")
    )

    # Create a dictionary to hold the data.
    transactions = defaultdict(list)

    # Loop over each movement.
    for movement in movements:
        # Retrieve the counterpart movements for each transaction.
        counterpart_movements = (
            Ledger.objects.filter(transaction_id_id=movement.transaction_id_id)
            .exclude(account_number_id=pk)
            .select_related("account_number")
        )

        # Loop over each counterpart movement
        # and append it to the transactions dictionary.
        for counterpart in counterpart_movements:
            transactions[movement.transaction_id_id].append(
                {
                    "amount": counterpart.amount,
                    "created_at": counterpart.created_at,
                    "account_number": counterpart.account_number.account_number,
                }
            )

    context = {"account": account, "transactions": dict(transactions)}

    return render(request, "best_bank_as/accounts/details.html", context)

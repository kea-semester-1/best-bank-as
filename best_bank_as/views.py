from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q, ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.crypto import get_random_string

from best_bank_as import decorators
from best_bank_as.enums import (
    AccountStatus,
    ApplicationStatus,
    CustomerRank,
    CustomerStatus,
)
from best_bank_as.forms.customer_form import (
    CustomerCreationForm,
    CustomerUpdateForm,
    UserCreationByEmployeeForm,
    UserCreationForm,
    UserUpdateForm,
)
from best_bank_as.forms.loan_application_form import LoanApplicationForm
from best_bank_as.forms.request_new_account_form import NewAccountRequestForm
from best_bank_as.forms.TransferForm import TransferForm
from best_bank_as.forms.external_transfer_form import ExternalTransferForm
from best_bank_as.models.account import Account
from best_bank_as.models.customer import Customer
from best_bank_as.models.ledger import Ledger
from best_bank_as.models.loan_application import LoanApplication
from project import settings

status_list = AccountStatus.name_value_pairs()
rank_list = CustomerRank.name_value_pairs()

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
def get_accounts_list(request: HttpRequest) -> HttpResponse:
    """Retrieve all accounts for a given user."""

    if request.method == "GET":
        customer = get_object_or_404(Customer, user=request.user)
        accounts = customer.get_accounts()
        context = {
            "accounts": accounts,
            "status_list": status_list,
        }
        return render(request, "best_bank_as/accounts/account_list.html", context)

    if request.method == "POST":
        form = NewAccountRequestForm(request.POST)
        if form.is_valid():
            request_status = request.POST.get("request_status")
            status = (
                AccountStatus.ACTIVE
                if request_status == AccountStatus.ACTIVE
                else AccountStatus.PENDING
            )
            pk = request.POST.get("customer_pk")

            if pk is None:
                customer = request.user.customer
            else:
                customer = get_object_or_404(Customer, pk=pk)

            try:
                new_account = Account.request_new_account(
                    customer=customer, status=status  # type: ignore
                )
                status_label = new_account.get_account_status_display()
            except Exception as e:
                context = {"error": str(e)}
                return render(
                    request, "best_bank_as/error_pages/error_page.html", context
                )

            response_text = (
                f"Status: {status_label},"
                f" Account number: {new_account.account_number}"
            )
            context = {"data": response_text}
            return render(
                request, "best_bank_as/accounts/request_account_partial.html", context
            )

    # Default context for GET request if not returned inside the IF block
    context = {}
    return render(request, "best_bank_as/accounts/account_list.html", context)


@login_required
def get_account_details(request: HttpRequest, pk: int) -> HttpResponse:
    """Retrieve information for a given account."""
    account = get_object_or_404(Account, pk=pk)

    context = {"account": account, "status_list": status_list}

    if request.user != account.customer.user and not request.user.is_staff:
        return HttpResponseForbidden(
            render(request, "best_bank_as/error_pages/error_page.html")
        )

    if request.method == "GET":
        balance = account.get_balance()
        transactions = account.get_transactions()

        context = {"balance": balance, "transactions": transactions}

    if request.method == "PUT" and request.user.is_staff:
        data = request.PUT
        value = data.get("account_status")
        try:
            account.update_account_status(value)
            account.refresh_from_db()
            messages.success(request, "Account status was successfully updated.")
        except Exception:  # TODO: Find more specific error
            messages.error(request, "Something went wrong. Please try again.")

        return render(
            request, "best_bank_as/accounts/account_status_partial.html", context
        )
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

    customers = (
        Customer.objects.filter(
            Q(phone_number__icontains=query) | Q(user__username__icontains=query)
        )
        .distinct()
        .select_related("user")  # join
        # .prefetch_related(Prefetch("account_set"))
    )

    context = {
        "customers": customers,
        "query": query,
        "status_list": status_list,
        "rank_list": rank_list,
        "updateForm": UserUpdateForm,
        "updateCustomerForm": CustomerUpdateForm,
    }
    return render(
        request,
        "best_bank_as/customers/customers_search.html",
        context,
    )


@decorators.group_required("customer")
def loan_application_list(request: HttpRequest) -> HttpResponse:
    """View for creating a new loan application."""

    customer = get_object_or_404(Customer, user=request.user)
    status_filter = request.GET.get("status_filter")

    if request.method == "POST":
        if not customer.can_loan:
            return render(
                request,
                "best_bank_as/error_pages/error_page.html",
            )

        form = LoanApplicationForm(data=request.POST, customer=customer)
        if not form.is_valid():
            return render(
                request,
                "best_bank_as/error_pages/error_page.html",
            )
        form_data = form.cleaned_data
        application = LoanApplication(
            reason=form_data["reason"],
            amount=form_data["amount"],
            status=ApplicationStatus.PENDING,
            customer=customer,
        )
        application.save()
        return redirect("best_bank_as:loan_application_list")

    context = {
        "customer": customer,
        "is_customer": True,
        "loan_applications": LoanApplication.filter_fmt(
            customer=customer, status=status_filter
        )
        if status_filter
        else customer.loan_applications,
        "form": LoanApplicationForm(customer=customer),
    }

    return render(
        request,
        "best_bank_as/loan_applications/customer_loan_applications_page.html",
        context,
    )


@decorators.group_required("employee", "supervisor")
def staff_loan_applications_page(request: HttpRequest) -> HttpResponse:
    """View for listing all loan applications."""

    status_filter = request.GET.get("status_filter")

    context = {
        "loan_applications": LoanApplication.filter_fmt(status=status_filter)
        if status_filter
        else LoanApplication.filter_fmt(),
        "is_customer": False,
    }

    return render(
        request,
        "best_bank_as/loan_applications/staff_loan_applications_page.html",
        context,
    )


@decorators.group_required("customer")
def loan_application_details(request: HttpRequest, pk: int) -> HttpResponse:
    """Retrieve information for a given loan application."""

    customer = get_object_or_404(Customer, user=request.user)
    application = get_object_or_404(LoanApplication, pk=pk)
    if application.customer != customer:
        return HttpResponseForbidden(
            render(request, "best_bank_as/error_pages/error_page.html")
        )

    if request.method == "DELETE":
        if application.status == ApplicationStatus.SUPERVISOR_APPROVED:
            return HttpResponseForbidden("Already approved by supervisor")

        application.delete()
        return redirect("best_bank_as:loan_application_list")

    context = {
        "is_customer": True,
        "loan_application": application,
        "status_name": application.status_name,
    }

    return render(
        request,
        "best_bank_as/loan_applications/loan_application_details.html",
        context,
    )


@decorators.group_required("employee", "supervisor")
def staff_loan_application_details(request: HttpRequest, pk: int) -> HttpResponse:
    """Retrieve information for a given loan application, as staff."""

    application = get_object_or_404(LoanApplication, pk=pk)

    if request.method == "DELETE":
        application.reject()
        return redirect("approve_loan_applications")

    user = request.user

    if request.method == "PUT":
        is_employee = not user.groups.filter(name="supervisor").exists()

        if is_employee and application.employee_approved:
            return HttpResponseForbidden("Already approved by employee")

        if is_employee:
            application.employee_approve(user)
        else:
            application.supervisor_approve(user)
            customer: Customer = application.customer
            customer.create_loan(application)
        return redirect("approve_loan_applications")

    context = {
        "loan_application": application,
        "status_name": application.status_name,
    }

    return render(
        request,
        "best_bank_as/loan_applications/loan_application_details.html",
        context,
    )


@login_required()
def transaction_list(request: HttpRequest) -> HttpResponse:  # TODO: Transaction naming
    """View to transfer money from account to account."""
    if request.method != "POST":
        return render(
            request,
            "best_bank_as/handle_funds/transfer-money.html",
            {"form": TransferForm(user=request.user)},
        )
    form = TransferForm(data=request.POST, user=request.user)
    if not form.is_valid():  # or throw exception
        logger.error(f"TransferForm is not valid. Errors: {form.errors}")
        return render(
            request,
            "best_bank_as/handle_funds/transfer-money.html",
            {"form": form},
        )
    source_account = form.cleaned_data["source_account"]
    destination_account = form.cleaned_data["destination_account"]
    registration_number = form.cleaned_data["registration_number"]
    amount = form.cleaned_data["amount"]

    if registration_number != "6666":
        Ledger.enqueue_external_transfer(
            source_account=source_account,
            destination_account=destination_account,
            amount=amount,
            registration_number=registration_number,
        )
        messages.success(request, "External transfer initiated successfully.")
    else:
        destination_account_instance = Account.objects.get(pk=destination_account)
        Ledger.transfer(
            source_account=source_account,
            destination_account=destination_account_instance,
            amount=amount,
        )
        messages.success(request, "Internal transfer completed successfully.")

    return redirect("best_bank_as:index")


def external_transfer(request: HttpRequest) -> HttpResponse:
    """View to handle incoming external money transfers."""
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    form = ExternalTransferForm(data=request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    # Extract validated data
    source_account_id = 1
    destination_account_id = form.cleaned_data["destination_account"]
    amount = form.cleaned_data["amount"]

    source_account = Account.objects.get(pk=source_account_id)
    destination_account = Account.objects.get(pk=source_account_id)

    # Validate and process the accounts

    destination_account = Account.objects.get(pk=destination_account_id)

    # Assuming Ledger.transfer is the method to transfer funds internally

    # Perform the transfer logic
    Ledger.transfer(
        source_account=source_account,  # Assuming this is an ID or external reference
        destination_account=destination_account,
        amount=amount,
    )
    return JsonResponse({"message": "Transfer completed successfully."}, status=200)


@login_required
def get_accounts_for_user(
    request: HttpRequest, pk: int
) -> HttpResponse:  # TODO: FIX LOGIC
    """Retrieve all accounts for a given user."""

    if not request.user.is_staff:
        return HttpResponseForbidden()

    customer = get_object_or_404(Customer, user=pk)

    accounts = customer.get_accounts()
    print(accounts)

    context = {"accounts": accounts}
    return render(request, "best_bank_as/accounts/account_list.html", context)


@decorators.group_required("employee")
def approve_customers_list(request: HttpRequest) -> HttpResponse:
    """Get all pending new customers."""
    customers = Customer.get_pending()
    return render(
        request,
        "best_bank_as/customers/customers_pending.html",
        {"customers": customers},
    )


def approve_customers_details(request: HttpRequest, pk: int) -> HttpResponse:
    """Update status on customer, from pending to: Approved or Rejected."""
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "PUT":
        customer.update_status(CustomerStatus.APPROVED)

    if request.method == "DELETE":
        customer.update_status(CustomerStatus.REJECTED)

    customers = Customer.get_pending()

    return render(
        request,
        "best_bank_as/customers/customers_table.html",
        {"customers": customers},
    )


@decorators.group_required("employee", "supervisor")
def customer_list(request: HttpRequest) -> HttpResponse:
    """Create a new customer profile."""
    if request.method == "GET":
        user_form = UserCreationForm()
        customer_form = CustomerCreationForm()

        if request.user.is_staff:
            user_form = UserCreationByEmployeeForm()
            context = {"userForm": user_form, "customerForm": customer_form}
            return render(
                request, "registration/customer_creation_employee.html", context
            )

    if request.method == "POST":
        if request.user.is_staff:
            user_form = UserCreationByEmployeeForm(request.POST)
            customer_form = CustomerCreationForm(request.POST)

            if user_form.is_valid() and customer_form.is_valid():
                # User instance
                new_user = user_form.save(commit=False)
                random_password = get_random_string(length=16)
                new_user.set_password(random_password)
                new_user.save()

                # Customer instance
                new_customer = customer_form.save(commit=False)
                new_customer.status = CustomerStatus.APPROVED
                new_customer.user = new_user
                new_customer.save()

                print(f"*** Sending email to {new_user.email} ***")
                send_mail(
                    subject="Welcome to Best Bank AS",
                    message=f"Your password is: '{random_password}' - "
                    "Make sure to reset it as soon as possible.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[new_user.email],
                )
        else:
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


def customer_details(request: HttpRequest, pk: int) -> HttpResponse:
    """Detail view for customers."""
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "PUT":
        customer_form = CustomerUpdateForm(request.PUT)
        user_form = UserUpdateForm(request.PUT)
        data = request.PUT
        customer_rank_value = data.get("customer_rank")

        if request.user.is_staff and customer_rank_value:
            try:
                customer.update_rank(customer_rank_value)
                customer.refresh_from_db()
                messages.success(request, "Customer rank successfully updated.")
            except Exception:  # TODO: Find more specific error
                messages.error(request, "Something went wrong. Please try again")

            context = {"customer": customer, "rank_list": rank_list}
            return render(
                request,
                "best_bank_as/customers/customer_rank_partial.html",
                context,
            )

        if customer_form.is_valid() and user_form.is_valid():
            customer.update_customer_fields(**customer_form.cleaned_data)
            customer.update_customer_fields(**user_form.cleaned_data)
            customer.refresh_from_db()
            messages.success(request, "Customer successfully updated.")
            context = {
                "customer": customer,
                "updateCustomerForm": CustomerUpdateForm,
                "updateForm": UserUpdateForm,
            }
            return render(
                request, "best_bank_as/customers/customer_update.html", context
            )

    if request.method == "DELETE":
        try:
            customer.set_customer_active_status()
            customer.refresh_from_db()
            messages.success(request, "Customer set as inactive")
            context = {"customer": customer}
        except Exception:  # TODO: Find more specific error
            messages.error(request, "Something went wrong. Please try again")

        return render(
            request, "best_bank_as/customers/customer_active_status.html", context
        )

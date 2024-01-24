import os
from decimal import Decimal
from typing import TYPE_CHECKING, Any

import django_rq
import requests
from django.db import models
from django.db.transaction import atomic
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from best_bank_as import enums
from best_bank_as.db_models.bank import Bank
from best_bank_as.db_models.core import base_model
from best_bank_as.db_models.transaction import Transaction
from best_bank_as.enums import AccountStatus
from uuid import uuid4


if TYPE_CHECKING:
    from best_bank_as.db_models.account import Account


class Ledger(base_model.BaseModel):
    """Model for ledger."""

    registration_number = models.ForeignKey(
        "best_bank_as.Bank", on_delete=models.CASCADE, default=1
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(
        choices=enums.TransactionStatus.choices,
        default=0,
    )
    account = models.ForeignKey(
        "Account",
        on_delete=models.CASCADE,
        null=True,
    )
    transaction = models.ForeignKey(
        "Transaction",
        on_delete=models.CASCADE,
        null=True,
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    @classmethod
    def transfer(
        cls, source_account: "Account", destination_account: "Account", amount: Decimal
    ) -> None:
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")

        if source_account == destination_account:
            raise ValueError(
                "Source account and destination account cannot be the same."
            )

        if destination_account.account_status == AccountStatus.PENDING:
            raise ValueError("Cannot transfer money to pending account.")

        # TODO: Handle this with better error page and handling.
        if source_account.get_balance() < amount:
            raise ValueError("Amount cannot be less than balance")
        new_transaction = Transaction.objects.create()

        # Source account
        cls.objects.create(
            amount=-amount,
            account=source_account,
            transaction=new_transaction,
        )

        # Destination account
        cls.objects.create(
            amount=amount,
            account=destination_account,
            transaction=new_transaction,
        )

    @classmethod
    @atomic
    def transfer_external(
        cls,
        source_account: Any,
        destination_reg_no: Any,
        destination_account: Any,
        amount: Decimal,
    ) -> int:
        if destination_reg_no is None:
            raise ValueError("Registration number must be input")

        if destination_account is None:
            raise ValueError("Destination account must be input")

        if amount <= 0:
            print(amount)
            raise ValueError("Amount must be a positive number.")

        # TODO: Handle this with better error page and handling.
        if source_account.get_balance() < amount:
            raise ValueError("Amount cannot be less than balance")

        try:
            bank = Bank.objects.get(reg_number=destination_reg_no)
        except Bank.DoesNotExist as e:
            raise e

        new_transaction = Transaction.objects.create()

        # Source account
        cls.objects.create(
            amount=-amount,
            account=source_account,
            transaction_id=new_transaction.id,
            registration_number=bank,
            status=enums.TransactionStatus.PENDING,
        )
        # Destination account the bank

        destination_account.id = 1
        cls.objects.create(
            amount=amount,
            account=destination_account,
            transaction=new_transaction,
        )
        return new_transaction.id

    @classmethod
    def enqueue_external_transfer(
        cls,
        source_account: Any,
        registration_number: Any,
        destination_account: Any,
        amount: Decimal,
    ) -> None:
        django_rq.enqueue(
            cls.initiate_external_transfer,
            amount=amount,
            source_account=source_account,
            destination_reg_no=registration_number,
            destination_account=destination_account,
        )

    @classmethod
    def set_status(cls, transaction_id: int, status: enums.TransactionStatus) -> None:
        ledger = cls.objects.filter(transaction_id=transaction_id)

        if ledger is None:
            raise ValueError("No ledger found")

        ledger.update(status=status)

    @classmethod
    def login_and_get_session(cls, reg_number: Any) -> requests.Session:
        """Login and get session, we also add retry strategy."""
        with requests.Session() as session:
            retries = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504],
            )
            session = requests.Session()
            adapter = HTTPAdapter(max_retries=retries)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            # GET request to fetch CSRF token
            bank = Bank.objects.get(reg_number=reg_number)
            login_url = f"{bank.url}/accounts/login/"
            initial_response = session.get(login_url)
            initial_response.raise_for_status()

            # Extract CSRF token from cookies
            csrf_token = session.cookies.get("csrftoken")

            if not csrf_token:
                raise ValueError("CSRF token not found in initial response")

            # POST request with CSRF token and credentials
            credentials = {
                "username": os.environ["USER_NAME"],
                "password": os.environ["PASSWORD"],
                "csrfmiddlewaretoken": csrf_token,
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": login_url,  # Adding the Referer header
                "X-CSRFToken": csrf_token,
            }

            login_response = session.post(
                url=login_url, data=credentials, headers=headers, allow_redirects=False
            )

            login_response.raise_for_status()

            # Return the session for subsequent authenticated requests
            return session

    @classmethod
    def initiate_external_transfer(
        cls,
        source_account: Any,
        destination_reg_no: Any,
        destination_account: Any,
        amount: Decimal,
    ) -> None:
        """Initiate the transfer to the external bank."""

        # form data
        data = {
            "source_account": source_account.id,
            "destination_account": destination_account.id,
            "registration_number": destination_reg_no,
            "amount": amount,
        }
        session = cls.login_and_get_session(reg_number=destination_reg_no)
        # URL of the external bank's `transaction_list` view
        bank = Bank.objects.get(reg_number=destination_reg_no)
        external_bank_url = f"{bank.url}/external-transfer/"
        csrf_token = session.cookies.get("csrftoken")
        idempotency_key = str(uuid4())
        try:
            transaction_id = cls.transfer_external(
                source_account, destination_reg_no, destination_account, amount
            )
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrf_token,
                "Idempotency-Key": idempotency_key,
            }

            response = session.post(
                external_bank_url,
                data=data,
                headers=headers,
            )

            response.raise_for_status()

            if response.status_code == 200:
                cls.finalize_external_transfer(
                    transaction_id=transaction_id,
                    status=enums.TransactionStatus.PROCESSED,
                )
        except requests.RequestException as e:
            print(e)

    @classmethod
    @atomic
    def finalize_external_transfer(
        cls,
        transaction_id: int,
        status: enums.TransactionStatus,
    ) -> None:
        """
        Finalize the external transfer by updating its status.
        """
        # Ensure the transaction exists
        if not Transaction.objects.filter(id=transaction_id).exists():
            raise ValueError("Transaction not found")

        cls.set_status(transaction_id=transaction_id, status=status)

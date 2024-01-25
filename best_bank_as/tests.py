from decimal import Decimal
import uuid

from django.contrib.auth.models import Group
from django.test import Client, TestCase
from django.urls import reverse
from django.core.management import call_command
from django.test import TestCase

from best_bank_as.db_models.account import Account
from best_bank_as.db_models.customer import Customer
from best_bank_as.db_models.ledger import Ledger
from best_bank_as.db_models.loan_application import LoanApplication
from best_bank_as.enums import AccountStatus, AccountType, CustomerRank
from best_bank_as.management.commands.provision import (
    create_groups,
    create_internal_bank_account,
)
from best_bank_as.models import CustomUser


class CustomerTestCase(TestCase):
    """Test case for customer model."""
    
    @classmethod
    def setUpTestData(cls) -> None:
        call_command('provision')
        call_command('demodata')

        # Create users and assign groups
        cls.employee_user = CustomUser.objects.create_user(username="employee")
        cls.supervisor_user = CustomUser.objects.create_user(username="supervisor")
        
        employee_group = Group.objects.get(name="employee")
        supervisor_group = Group.objects.get(name="supervisor")
        cls.employee_user.groups.add(employee_group)
        cls.supervisor_user.groups.add(supervisor_group)


        # Create a customer and accounts
        cls.user = CustomUser.objects.create_user(
            username="testuser", email="tester@gmail.com", password="test123"
        )
        cls.customer = Customer.objects.create(user=cls.user, phone_number="11223344")
        cls.account1 = Account.objects.create(
            customer=cls.customer,
            account_type=AccountType.SAVINGS,
            account_status=AccountStatus.ACTIVE,
        )
        cls.account2 = Account.objects.create(
            customer=cls.customer,
            account_type=AccountType.SAVINGS,
            account_status=AccountStatus.ACTIVE,
        )

        # Create an internal bank account and transfer funds to the customer
        internal_account = Account.objects.get(account_type=AccountType.INTERNAL)
        Ledger.transfer(internal_account, cls.account1, Decimal(1000))

    def test_customer_has_two_accounts(self) -> None:
        """Customers should have exactly two accounts."""
        self.assertEqual(len(self.customer.get_accounts()), 2)

    def test_account_initial_balance(self) -> None:
        """Account balance should start at 1000."""
        self.assertEqual(self.account1.get_balance(), 1000)

    def test_transfer_between_accounts(self) -> None:
        """Transfer should correctly move funds between accounts."""
        Ledger.transfer(self.account1, self.account2, Decimal(100))
        self.assertEqual(self.account2.get_balance(), 100)
        self.assertEqual(self.account1.get_balance(), 900)

    def test_request_new_account_creates_pending_account(self) -> None:
        """Requesting a new account should create an account with pending status."""
        new_account = Account.request_new_account(
            customer=self.customer, status=AccountStatus.PENDING  # type: ignore
        )
        self.assertEqual(new_account.account_status, AccountStatus.PENDING)

    def test_customer_with_gold_rank_can_loan(self) -> None:
        """Gold rank customers should be eligible for loans."""
        self.customer.rank = CustomerRank.GOLD
        self.assertTrue(self.customer.can_loan)

    def test_loan_application_and_approval_creates_loan(self) -> None:
        """Approving a loan application should create a new loan."""
        self.customer.rank = CustomerRank.GOLD
        loan_application = LoanApplication.objects.create(
            reason="Test", amount=1000, customer=self.customer
        )
        loan_application.employee_approve(self.employee_user)
        loan_application.supervisor_approve(self.supervisor_user)
        self.customer.create_loan(loan_application=loan_application)
        self.assertEqual(len(self.customer.get_accounts()), 3)



    def test_user_can_login_and_transfer(self) -> None:
        c = Client()

        # Login
        response = c.get("/accounts/login/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
        response = c.post(
            "/accounts/login/",
            {"username": self.user.username, "password": self.user.password},
            follow=True,
        )
        assert response.status_code == 200
        self.assertTemplateUsed(response, "registration/login.html")

        # Go to profile
        response = c.get(f"/profile/", follow=True)
        assert response.status_code == 200

        # Transfer
        headers = {
            "Idempotency-Key": str(uuid.uuid4()),
        }
        response = c.post(
            "/transfer/",
            {
                "source_account": self.account1,
                "deination_account": self.account2,
                "registration_number": "6666",
                "amount": 100,
            },
            headers=headers,
            follow=True,
        )
        
        assert response.status_code == 200
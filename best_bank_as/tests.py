# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth.models import User
from best_bank_as import enums
from best_bank_as.forms.TransferForm import TransferForm
from best_bank_as.management.commands.provision import create_groups
from best_bank_as.models.account import Account
from best_bank_as.models.customer import Customer
from best_bank_as.models.ledger import Ledger
from best_bank_as.models.transaction import Transaction
from best_bank_as.models.loan_application import LoanApplication
from best_bank_as.models.loan import Loan
from best_bank_as.enums import AccountType, AccountStatus, CustomerRank, LoanStatus, ApplicationStatus
from django.contrib.auth.models import Group



class CustomerTestCase(TestCase):
    def setUp(self):
        
        create_groups()
        
        employee_group = Group.objects.get(name='employee') 
        supervisor_group = Group.objects.get(name='supervisor') 
        
        # Create employee user
        employee_user = User.objects.create_user(username="employee")
        employee_group.user_set.add(employee_user)
        self.employee_user = employee_user
        
        # Create supervisor user
        supervisor_user = User.objects.create_user(username="supervisor")
        supervisor_group.user_set.add(supervisor_user)
        self.supervisor_user = supervisor_user
        
        
        
        # Create bank internal account
        bank = Account.objects.create(
        account_type=enums.AccountType.INTERNAL,
        account_status=enums.AccountStatus.ACTIVE,
        customer=None,
        )

        transaction = Transaction.objects.create()

        # Add starting balance
        Ledger.objects.create(
            account=bank,
            transaction=transaction,
            amount=1000000,
        )
        
        # Create customer
        user = User.objects.create_user(username="test", email="tester@gmail.com", password="test123")
        customer = Customer.objects.create(user=user, phone_number="11223344")
        
        # Create customer accounts
        customer_account_1 = Account.objects.create(customer=customer, account_type=AccountType.SAVINGS, account_status=AccountStatus.ACTIVE)
        customer_account_2 = Account.objects.create(customer=customer, account_type=AccountType.SAVINGS, account_status=AccountStatus.ACTIVE)
        
        Ledger.transfer(bank, customer_account_1, 1000)
        
        self.account1 = customer_account_1
        self.account2 = customer_account_2
        self.user = user
        self.customer = customer
    

    def test_get_accounts(self):
        """Test get accounts."""
        self.assertEqual(len(self.customer.get_accounts()), 2)
        
    def test_get_balance(self):
        """Test get balance."""
        self.assertEqual(self.account1.get_balance(), 1000)
        
    def test_can_make_transfer(self):
        """Test can make transfer."""
        Ledger.transfer(self.account1, self.account2, 100)
        
        self.assertEqual(self.account2.get_balance(), 100)
        self.assertEqual(self.account1.get_balance(), 900)
        
    def test_can_request_new_account(self):
        """Test can request new account."""
        new_account = Account.request_new_account(customer=self.customer, status=AccountStatus.PENDING)
        
        self.assertEqual(new_account.account_status, AccountStatus.PENDING)
        self.assertEqual(new_account.account_type, AccountType.SAVINGS)
        self.assertEqual(new_account.customer, self.customer)
        
        
    def test_can_make_loan(self):
        self.customer.rank = CustomerRank.GOLD
        self.assertEqual(self.customer.can_loan, True)
        
    def test_make_laon(self):
        self.customer.rank = CustomerRank.GOLD
        self.customer.save()
        
        loan_application = LoanApplication.objects.create(
            reason="Test",
            amount=1000,
            customer=self.customer,
        )        
        
        loan_application.employee_approve(self.employee_user)
        loan_application.supervisor_approve(self.supervisor_user)
        
        self.customer.create_loan(loan_application=loan_application)
        
        self.assertEqual(len(self.customer.get_accounts()), 3)
        
    # def test_user_can_login_and_transfer(self):
    #     c = Client()
    #     response = c.get('/accounts/login/', follow=True)
    #     self.assertTemplateUsed(response, "registration/login.html")
    #     response = c.post('/accounts/login/', 
    #                       { 'username': self.user.username, 'password': self.user.password }, follow=True)
    #     assert response.status_code == 200
    #     self.assertTemplateUsed(response, "registration/login.html")
        
    #     response = c.get(f'/profile/{self.user.username}', follow=True)  # Go to profile page
    #     assert response.status_code == 200
        
    
    #     response = c.post(f"transfer/", 
    #                       {
    #                           "source_account": self.account1.id,
    #                           "deination_account": self.account2.id,
    #                           "amount": 100
    #                       }, follow=True)
        
        
        
    #     #print(self.account1.get_balance())
    #     #print(self.account2.get_balance())
    #     #self.assertEqual(self.account2.get_balance(), 100)
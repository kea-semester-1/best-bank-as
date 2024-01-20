from django.contrib import admin

from best_bank_as.models.account import Account
from best_bank_as.models.account_type import AccountType
from best_bank_as.models.customer import Customer
from best_bank_as.models.ledger import Ledger
from best_bank_as.models.loan import Loan
from best_bank_as.models.loan_application import LoanApplication
from best_bank_as.models.transaction import Transaction

# Register your models here.


admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(Transaction)
admin.site.register(Ledger)
admin.site.register(LoanApplication)
admin.site.register(Loan)
